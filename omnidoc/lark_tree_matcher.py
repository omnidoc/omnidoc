from collections import defaultdict

from lark.tree import Tree
from lark.common import ParserConf
from lark.lexer import Token
from lark.parsers import earley
from lark.grammar import Rule, Terminal, NonTerminal


def is_discarded_terminal(t):
    return t.is_term and t.filter_out

def is_iter_empty(i):
    try:
        _ = next(i)
        return False
    except StopIteration:
        return True


class MakeTreeMatch:
    def __init__(self, name, expansion):
        self.name = name
        self.expansion = expansion

    def __call__(self, args):
        t = Tree(self.name, args)
        t.meta.match_tree = True
        t.meta.orig_expansion = self.expansion
        return t

def best_from_group(seq, group_key, cmp_key):
    d = {}
    for item in seq:
        key = group_key(item)
        if key in d:
            v1 = cmp_key(item)
            v2 = cmp_key(d[key])
            if v2 > v1:
                d[key] = item
        else:
            d[key] = item
    return list(d.values())

def _match(term, token):
    if isinstance(token, Tree):
        name, _args = parse_rulename(term.name)
        return token.data == name
    elif isinstance(token, Token):
        return term == Terminal(token.type)
    assert False

def make_recons_rule(origin, expansion, old_expansion):
    return Rule(origin, expansion, alias=MakeTreeMatch(origin.name, old_expansion))

def make_recons_rule_to_term(origin, term):
    return make_recons_rule(origin, [Terminal(term.name)], [term])

import re
def parse_rulename(s):
    name, args_str = re.match('(\w+)(?:{(.+)})?', s).groups()
    args = args_str and [a.strip() for a in args_str.split(',')]
    return name, args

class TreeMatcher:
    def __init__(self, parser):
        # XXX TODO calling compile twice returns different results!
        assert parser.options.maybe_placeholders == False
        tokens, rules, _grammar_extra = parser.grammar.compile(parser.options.start)

        self.rules_for_root = defaultdict(list)

        self.rules = list(self._build_recons_rules(rules))
        self.rules.reverse()

        # Choose the best rule from each group of {rule => [rule.alias]}, since we only really need one derivation.
        self.rules = best_from_group(self.rules, lambda r: r, lambda r: -len(r.expansion))

        self.rules.sort(key=lambda r: len(r.expansion))
        self.parser = parser
        self._parser_cache = {}

    def _build_recons_rules(self, rules):
        expand1s = {r.origin for r in rules if r.options.expand1}

        aliases = defaultdict(list)
        for r in rules:
            if r.alias:
                aliases[r.origin].append( r.alias )

        rule_names = {r.origin for r in rules}
        nonterminals = {sym for sym in rule_names
                        if sym.name.startswith('_') or sym in expand1s or sym in aliases }

        seen = set()
        for r in rules:
            recons_exp = [sym if sym in nonterminals else Terminal(sym.name)
                          for sym in r.expansion if not is_discarded_terminal(sym)]

            # Skip self-recursive constructs
            if recons_exp == [r.origin] and r.alias is None:
                continue

            sym = NonTerminal(r.alias) if r.alias else r.origin
            rule = make_recons_rule(sym, recons_exp, r.expansion)

            if sym in expand1s and len(recons_exp) != 1:
                self.rules_for_root[sym.name].append(rule)

                if sym.name not in seen:
                    yield make_recons_rule_to_term(sym, sym)
                    seen.add(sym.name)
            else:
                if sym.name.startswith('_') or sym in expand1s:
                    yield rule
                else:
                    self.rules_for_root[sym.name].append(rule)

        for origin, rule_aliases in aliases.items():
            for alias in rule_aliases:
                yield make_recons_rule_to_term(origin, NonTerminal(alias))
            yield make_recons_rule_to_term(origin, origin)

    def match_tree(self, tree, rulename):
        if rulename:
            # validate
            name, _args = parse_rulename(rulename)
            assert tree.data == name
        else:
            rulename = tree.data

        # TODO: ambiguity?
        try:
            parser = self._parser_cache[rulename]
        except KeyError:
            rules = self.rules + best_from_group(
                self.rules_for_root[rulename], lambda r: r, lambda r: -len(r.expansion)
            )

            rules.sort(key=lambda r: len(r.expansion))

            callbacks = {rule: rule.alias for rule in rules}  # TODO pass callbacks through dict, instead of alias?
            parser = earley.Parser(ParserConf(rules, callbacks, [rulename]), _match, resolve_ambiguity=True)
            self._parser_cache[rulename] = parser

        unreduced_tree = parser.parse(tree.children, rulename)   # find a full derivation
        assert unreduced_tree.data == rulename
        return unreduced_tree