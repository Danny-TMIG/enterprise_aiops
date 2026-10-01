#!/usr/bin/env python3
"""Generate DendriticSeeds from the Grammar taxonomy.
Self-contained: falls back to embedded GRAMMAR when no file is given."""
import json, re, sys
from pathlib import Path

GRAMMAR = r"""
· Grammar
  · Phonology
    · Phoneme
      · Consonant
        · Plosive
        · Fricative
        · Affricate
        · Nasal
        · Liquid
        · Glide
        · Trill
        · Tap
        · Flap
        · Lateral
      · Vowel
        · Monophthong
        · Diphthong
        · Triphthong
        · Close
        · Near-close
        · Close-mid
        · Mid
        · Open-mid
        · Near-open
        · Open
        · Front
        · Central
        · Back
        · Rounded
        · Unrounded
    · Allophone
    · Feature
      · Voicing
      · Place
      · Manner
      · Height
      · Backness
      · Rounding
      · Nasality
      · Aspiration
      · Length
      · Tone
      · Stress
    · Syllable
      · Onset
      · Nucleus
      · Coda
      · Rhyme
      · Heavy
      · Light
      · Open
      · Closed
    · Phonotactics
    · Prosody
      · Stress
      · Pitch
      · Tone
      · Intonation
      · Rhythm
      · Juncture
      · Timing
    · Morphophonology
      · Sandhi
      · Assimilation
      · Dissimilation
      · Elision
      · Epenthesis
      · Metathesis
      · Reduplication
      · Alternation
      · Suppletion
  · Morphology
    · Morpheme
      · Free
      · Bound
      · Root
      · Stem
      · Base
      · Affix
        · Prefix
        · Suffix
        · Infix
        · Circumfix
        · Transfix
        · Simulfix
        · Suprafix
        · Interfix
        · Duplifix
      · Clitic
        · Proclitic
        · Enclitic
        · Mesoclitic
        · Endoclitic
      · Allomorph
      · Zero
      · Portmanteau
      · Cranberry
    · Inflection
      · Declension
      · Conjugation
      · Agreement
      · Case
      · Number
      · Gender
      · Person
      · Tense
      · Aspect
      · Mood
      · Voice
      · Polarity
      · Definiteness
      · Comparison
      · Honorific
      · Evidential
      · Mirative
    · Derivation
      · Nominalization
      · Verbalization
      · Adjectivization
      · Adverbialization
      · Diminution
      · Augmentation
      · Negation
      · Causativization
      · Passivization
      · Antipassivization
      · Applicativization
      · Reflexivization
      · Reciprocization
      · Incorporation
    · Compounding
      · Endocentric
      · Exocentric
      · Copulative
      · Appositional
      · Determinative
      · Synthetic
      · Asynthetic
      · Compound noun
      · Compound verb
      · Compound adjective
      · Compound adverb
      · Compound preposition
    · Conversion
    · Reduplication
    · Suppletion
    · Alternation
    · Apophony
    · Umlaut
    · Ablaut
    · Metathesis
    · Haplology
    · Elision
    · Epenthesis
    · Prothesis
    · Paragoge
    · Syncope
    · Apocope
    · Aphaeresis
    · Synaeresis
    · Diaeresis
    · Assimilation
    · Dissimilation
    · Lenition
    · Fortition
    · Palatalization
    · Velarization
    · Labialization
    · Nasalization
    · Aspiration
    · Deaspiration
    · Voicing
    · Devoicing
    · Flapping
    · Tapping
    · Trilling
    · Spirantization
    · Affrication
    · Glottalization
    · Tonogenesis
    · Sandhi
  · Syntax
    · Word
      · Word class
        · Open class
          · Noun
            · Common noun
            · Proper noun
            · Count noun
            · Mass noun
            · Collective noun
            · Concrete noun
            · Abstract noun
            · Animate noun
            · Inanimate noun
            · Human noun
            · Nonhuman noun
            · Relational noun
            · Kin noun
            · Body-part noun
            · Locative noun
            · Temporal noun
            · Verbal noun
            · Gerund
            · Infinitive noun
            · Deverbal noun
            · Deadjectival noun
            · Compound noun
            · Simple noun
            · Derived noun
            · Zero-derived noun
            · Diminutive noun
            · Augmentative noun
            · Classifier noun
            · Noun feature
              · Number
              · Case
              · Gender
              · Definiteness
              · Animacy
              · Person
              · Honorific
              · Classifier
              · Countability
              · Alienability
              · Noun class
          · Verb
            · Lexical verb
            · Auxiliary verb
            · Primary auxiliary
            · Modal auxiliary
            · Copula
            · Light verb
            · Control verb
            · Raising verb
            · ECM verb
            · Small clause verb
            · Impersonal verb
            · Weather verb
            · Existential verb
            · Possessive verb
            · Copular verb
            · Transitive verb
            · Intransitive verb
            · Ditransitive verb
            · Ambitransitive verb
            · Complex transitive verb
            · Prepositional verb
            · Phrasal verb
            · Prepositional phrasal verb
            · Particle verb
            · Dynamic verb
            · Stative verb
            · Telic verb
            · Atelic verb
            · Punctual verb
            · Durative verb
            · Achievement verb
            · Accomplishment verb
            · Activity verb
            · Semelfactive verb
            · Iterative verb
            · Causative verb
            · Inchoative verb
            · Factitive verb
            · Resultative verb
            · Denominal verb
            · Deadjectival verb
            · Deverbal verb
            · Regular verb
            · Irregular verb
            · Strong verb
            · Weak verb
            · Finite verb
            · Nonfinite verb
              · Infinitive
              · Gerund
              · Participle
                · Present participle
                · Past participle
              · Supine
            · Verb feature
              · Tense
              · Aspect
              · Mood
              · Voice
              · Person
              · Number
              · Gender
              · Polarity
              · Finiteness
              · Evidentiality
              · Mirativity
              · Honorific
              · Transitivity
              · Valency
              · Argument structure
          · Adjective
            · Descriptive adjective
            · Qualitative adjective
            · Relational adjective
            · Classifying adjective
            · Gradable adjective
            · Non-gradable adjective
            · Absolute adjective
            · Extreme adjective
            · Comparative adjective
            · Superlative adjective
            · Positive adjective
            · Attributive adjective
            · Predicative adjective
            · Postpositive adjective
            · Appositive adjective
            · Substantive adjective
            · Nominal adjective
            · Participial adjective
            · Deverbal adjective
            · Denominal adjective
            · Deadjectival adjective
            · Compound adjective
            · Simple adjective
            · Derived adjective
            · Proper adjective
            · Quantitative adjective
            · Demonstrative adjective
            · Possessive adjective
            · Interrogative adjective
            · Relative adjective
            · Indefinite adjective
            · Distributive adjective
            · Adjective feature
              · Degree
              · Comparison
              · Inflection
              · Order
              · Scope
              · Intersectivity
              · Subsectivity
              · Scalarity
              · Subjectivity
          · Adverb
            · Manner
            · Time
            · Place
            · Frequency
            · Degree
            · Sentence adverb
            · Conjunctive adverb
            · Relative adverb
            · Interrogative adverb
            · Negative adverb
            · Evaluative adverb
            · Domain adverb
            · Speech-act adverb
            · Epistemic adverb
            · Evidential adverb
            · Focus adverb
            · Aspectual adverb
            · Adverb feature
              · Gradability
              · Scope
              · Position
              · Orientation
        · Closed class
          · Pronoun
            · Personal
            · Possessive
            · Reflexive
            · Reciprocal
            · Demonstrative
            · Relative
            · Interrogative
            · Indefinite
            · Negative
            · Universal
            · Existential
            · Anaphoric
            · Cataphoric
            · Expletive
            · Clitic
          · Determiner
            · Article
              · Definite
              · Indefinite
            · Demonstrative
            · Quantifier
            · Possessive
            · Numeral
            · Distributive
            · Interrogative
            · Relative
            · Exclamative
          · Preposition
            · Spatial
            · Temporal
            · Directional
            · Benefactive
            · Instrumental
            · Comitative
            · Agentive
            · Possessive
            · Comparative
            · Causal
            · Purpose
            · Manner
          · Postposition
          · Conjunction
            · Coordinating
            · Subordinating
            · Correlative
          · Auxiliary
          · Modal
          · Copula
          · Negator
          · Complementizer
          · Particle
          · Classifier
          · Interjection
          · Numeral
          · Quantifier
    · Phrase
      · Noun phrase
      · Verb phrase
      · Adjective phrase
      · Adverb phrase
      · Prepositional phrase
      · Postpositional phrase
      · Determiner phrase
      · Complementizer phrase
      · Inflection phrase
      · Tense phrase
      · Aspect phrase
      · Voice phrase
      · Negation phrase
      · Quantifier phrase
      · Numeral phrase
      · Classifier phrase
      · Focus phrase
      · Topic phrase
      · Mood phrase
      · Modal phrase
      · Agreement phrase
      · Case phrase
      · Possessive phrase
      · Gerund phrase
      · Infinitive phrase
      · Participle phrase
      · Small clause
      · Predicate phrase
    · Clause
      · Main
      · Independent
      · Subordinate
      · Dependent
      · Complement clause
        · Declarative complement
        · Interrogative complement
        · Infinitive complement
        · Gerund complement
        · Participial complement
        · Small clause complement
      · Relative clause
        · Restrictive
        · Nonrestrictive
        · Finite
        · Nonfinite
        · Free relative
        · Headed relative
        · Reduced relative
      · Adverbial clause
        · Time
        · Place
        · Manner
        · Reason
        · Purpose
        · Result
        · Condition
        · Concession
        · Comparison
        · Proportion
      · Comparative clause
      · Declarative
      · Interrogative
        · Polar
        · Wh-
        · Alternative
        · Tag
      · Imperative
      · Exclamative
      · Optative
      · Conditional
      · Cleft
      · Pseudo-cleft
      · Existential
      · Copular
      · Passive
      · Active
      · Middle
      · Antipassive
      · Applicative
      · Causative
      · Serial verb
      · Coordinate
      · Compound
      · Complex
      · Compound-complex
      · Finite
      · Nonfinite
      · Small clause
      · Matrix
      · Embedded
      · Root
      · Complement
      · Adjunct
      · Specifier
    · Sentence
      · Simple
      · Compound
      · Complex
      · Compound-complex
      · Declarative
      · Interrogative
      · Imperative
      · Exclamative
      · Optative
      · Fragment
      · Elliptical
      · Cleft
      · Pseudo-cleft
      · Existential
      · Passive
      · Active
      · Negative
      · Affirmative
    · Clause function
      · Subject
      · Predicate
        · Verbal predicate
        · Nominal predicate
        · Adjectival predicate
        · Adverbial predicate
        · Copular predicate
        · Complex predicate
        · Secondary predicate
        · Primary predicate
        · Matrix predicate
        · Embedded predicate
        · Small clause predicate
        · Existential predicate
        · Locative predicate
        · Possessive predicate
        · Weather predicate
        · Impersonal predicate
        · Control predicate
        · Raising predicate
        · ECM predicate
        · Factitive predicate
        · Resultative predicate
        · Depictive predicate
        · Stage-level predicate
        · Individual-level predicate
        · Kind-level predicate
      · Object
        · Direct object
        · Indirect object
        · Prepositional object
        · Cognate object
        · Retained object
        · Secondary object
      · Complement
        · Subject complement
        · Object complement
        · Adverbial complement
        · Prepositional complement
        · Infinitive complement
        · Gerund complement
        · Participial complement
        · Clausal complement
      · Adjunct
        · Adverbial adjunct
        · Adjectival adjunct
        · Nominal adjunct
        · Prepositional adjunct
        · Clausal adjunct
      · Modifier
      · Head
      · Specifier
      · Determiner
      · Predicator
      · Operator
      · Topic
      · Focus
      · Given
      · New
      · Theme
      · Rheme
      · Comment
    · Grammatical relation
      · Subject
      · Predicate
      · Object
      · Complement
      · Adjunct
      · Modifier
      · Head
      · Specifier
      · Determiner
    · Thematic role
      · Agent
      · Patient
      · Theme
      · Experiencer
      · Recipient
      · Goal
      · Source
      · Location
      · Instrument
      · Benefactive
      · Causative
      · Stimulus
      · Possessor
      · Possessum
      · Material
      · Product
      · Path
      · Direction
      · Extent
      · Measure
      · Time
      · Reason
      · Purpose
      · Manner
      · Means
      · Comitative
      · Privative
      · Prolative
      · Perlative
      · Ablative
      · Allative
      · Lative
      · Terminative
      · Semblative
      · Essive
      · Translative
      · Exessive
      · Instructive
      · Abessive
      · Adessive
      · Inessive
      · Elative
      · Illative
      · Superessive
      · Subessive
      · Sublative
      · Delative
      · Temporal
      · Causal
      · Final
      · Modal
      · Conditional
      · Concessive
      · Consecutive
      · Comparative
      · Equative
    · Syntactic operation
      · Agreement
      · Government
      · Case assignment
      · Movement
        · Wh-movement
        · NP-movement
        · Head movement
        · A-movement
        · A-bar movement
        · Scrambling
        · Topicalization
        · Focus movement
        · Extraposition
        · Raising
        · Control
        · Tough-movement
        · Passivization
        · Reflexivization
        · Clitic climbing
        · Verb second
        · Inversion
        · Subject-aux inversion
        · Do-support
      · Binding
        · Anaphor
        · Pronoun
        · R-expression
        · Binding domain
        · C-command
      · Control
      · Raising
      · ECM
      · Small clause
      · Ellipsis
        · VP ellipsis
        · NP ellipsis
        · Gapping
        · Stripping
        · Sluicing
        · Fragment
        · Null complement anaphora
      · Coordination
      · Subordination
      · Negation
      · Modality
      · Information structure
  · Semantics
    · Reference
    · Sense
    · Denotation
    · Connotation
    · Predication
    · Quantification
    · Scope
    · Binding
    · Tense
    · Aspect
    · Mood
    · Modality
    · Evidentiality
    · Presupposition
    · Entailment
    · Implicature
    · Truth conditions
    · Compositionality
    · Thematic roles
    · Event structure
    · Lexical semantics
    · Formal semantics
    · Cognitive semantics
    · Frame semantics
    · Prototype semantics
    · Componential analysis
    · Field theory
    · Sense relation
      · Synonymy
      · Antonymy
      · Hyponymy
      · Hypernymy
      · Meronymy
      · Holonymy
      · Polysemy
      · Homonymy
      · Homophony
      · Homography
      · Metonymy
      · Metaphor
  · Pragmatics
    · Speech act
      · Locutionary
      · Illocutionary
      · Perlocutionary
      · Direct
      · Indirect
    · Implicature
      · Conversational
      · Conventional
      · Scalar
      · Particularized
      · Generalized
    · Presupposition
    · Deixis
      · Person
      · Time
      · Place
      · Discourse
      · Social
    · Politeness
    · Face
    · Relevance
    · Context
    · Common ground
    · Information structure
    · Givenness
    · Topic
    · Focus
    · Contrast
    · Theme
    · Rheme
    · Cohesion
    · Coherence
  · Discourse
    · Text
    · Conversation
    · Turn-taking
    · Adjacency pair
    · Repair
    · Genre
    · Register
    · Style
    · Cohesion
    · Coherence
    · Anaphora
    · Cataphora
    · Exophora
    · Endophora
    · Topic chain
    · Paragraph
    · Narrative
    · Exposition
    · Argumentation
    · Description
  · Theoretical grammar
    · Traditional grammar
    · Structural grammar
    · Generative grammar
      · Standard theory
      · Extended standard theory
      · Government and binding
      · Minimalism
    · Dependency grammar
    · Construction grammar
    · Cognitive grammar
    · Functional grammar
    · Systemic functional grammar
    · Lexical-functional grammar
    · Head-driven phrase structure grammar
    · Categorial grammar
    · Tree adjoining grammar
    · Optimality theory
    · Role and reference grammar
    · Word grammar
    · Universal grammar
    · Montague grammar
    · Generalized phrase structure grammar
    · Relational grammar
    · Stratificational grammar
    · Tagmemics
    · Prague school
    · Copenhagen school
    · London school
    · American structuralism
    · Descriptivism
    · Prescriptivism
    · Pedagogical grammar
    · Comparative grammar
    · Historical grammar
    · Synchronic grammar
    · Diachronic grammar
    · Language-specific grammar
"""


def parse_grammar(text):
    root = {"name": "Grammar", "children": [], "level": -1}
    stack = [root]
    for line in text.splitlines():
        s = line.rstrip()
        if not s.strip() or not s.lstrip().startswith("·"):
            continue
        indent = len(s) - len(s.lstrip())
        level = indent // 2
        name = s.lstrip()[1:].strip()
        if not name:
            continue
        while len(stack) > 1 and stack[-1]["level"] >= level:
            stack.pop()
        parent = stack[-1]
        node = {"name": name, "children": [], "level": level}
        parent["children"].append(node)
        stack.append(node)
    if len(root["children"]) == 1:
        return root["children"][0]
    return root


def slug(s):
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")


def letters(s):
    return re.sub(r"[^A-Za-z]", "", s).upper()


def make_seed(node, path, parent_id, sibling_names):
    label = node["name"]
    full_path = path + [label]
    seed_id = ".".join(slug(p) for p in full_path)
    word = letters(label) or "XXX"
    if len(word) < 3:
        word = word + "X" * (3 - len(word))
    parent_name = path[-1] if path else "Grammar"
    return {
        "id": seed_id, "label": label, "path": full_path,
        "depth": len(full_path) - 1, "parent": parent_id,
        "delta": {"distinguishes": label,
                  "from": [s for s in sibling_names if s != label]},
        "pi": seed_id,
        "lambda": {"parent": parent_id, "children": [],
                   "siblings": [s for s in sibling_names if s != label]},
        "tau": {"config_ops": ["place", "link", "clue", "orient"],
                "reconfig_ops": ["move", "relink", "reclue", "rotate", "swap"]},
        "epsilon": {"clue": f"{parent_name} subtype: {label}",
                    "defining_criteria": [label.lower()]},
        "crossword": {"word": word, "length": len(word),
                      "clue": f"{parent_name} subtype: {label}",
                      "cells": [], "intersects": []},
        "config": {"state": "UNKNOWN", "grid": None,
                   "position": None, "orientation": None},
        "reconfig": {"transitions": [["UNKNOWN","PASS"],["UNKNOWN","FAIL"],
                                     ["PASS","CONFLICT"],["FAIL","CONFLICT"],
                                     ["CONFLICT","UNKNOWN"]],
                     "ir": {"op": "seed", "id": seed_id, "path": full_path}},
        "dendrite": {"root": "grammar", "branch_points": [], "terminals": []},
    }


def walk(node, path, parent_id, sibling_names, seeds):
    seed = make_seed(node, path, parent_id, sibling_names)
    seeds.append(seed)
    child_names = [c["name"] for c in node.get("children", [])]
    full_path = path + [node["name"]]
    for child in node.get("children", []):
        child_path = full_path + [child["name"]]
        child_id = ".".join(slug(p) for p in child_path)
        seed["lambda"]["children"].append(child_id)
        walk(child, full_path, seed["id"], child_names, seeds)


def anchor_branch_points(seed):
    w = seed["crossword"]["word"]
    seed["dendrite"]["branch_points"] = [
        {"pos": i, "letter": w[i]} for i in range(len(w))
    ]


def build_dendrite_graph(seeds):
    by_id = {s["id"]: s for s in seeds}
    for s in seeds:
        edges = []
        if s["parent"] and s["parent"] in by_id:
            edges.append({"to": s["parent"], "kind": "parent"})
        for c in s["lambda"]["children"]:
            if c in by_id:
                edges.append({"to": c, "kind": "child"})
        for sib_name in s["lambda"]["siblings"]:
            sib_path = s["path"][:-1] + [sib_name]
            sib_id = ".".join(slug(p) for p in sib_path)
            if sib_id in by_id:
                edges.append({"to": sib_id, "kind": "sibling"})
        s["dendrite"]["terminals"] = edges


def build_crossword_anchors(seeds):
    by_length, by_first, by_last, by_letter = {}, {}, {}, {}
    for s in seeds:
        w = s["crossword"]["word"]
        by_length.setdefault(len(w), []).append(s["id"])
        by_first.setdefault(w[0], []).append(s["id"])
        by_last.setdefault(w[-1], []).append(s["id"])
        for ch in set(w):
            by_letter.setdefault(ch, []).append(s["id"])
    return {"by_length": by_length, "by_first": by_first,
            "by_last": by_last, "by_letter": by_letter}


def build_real_crossword(seeds, n=200):
    placed, grid, used = [], {}, set()
    if not seeds:
        return placed, grid
    first = seeds[0]
    w = first["crossword"]["word"]
    placed.append({"id": first["id"], "word": w,
                   "clue": first["crossword"]["clue"],
                   "row": 0, "col": 0, "orientation": "across"})
    for i, ch in enumerate(w):
        grid[(0, i)] = ch
    used.add(first["id"])
    for seed in seeds[1:]:
        if len(placed) >= n:
            break
        if seed["id"] in used:
            continue
        w = seed["crossword"]["word"]
        done = False
        for i, ch in enumerate(w):
            for (r, c), existing in grid.items():
                if existing != ch:
                    continue
                start_r = r - i
                ok = True
                for j, wch in enumerate(w):
                    cell = (start_r + j, c)
                    if cell in grid and grid[cell] != wch:
                        ok = False
                        break
                if not ok:
                    continue
                for j, wch in enumerate(w):
                    grid[(start_r + j, c)] = wch
                placed.append({"id": seed["id"], "word": w,
                               "clue": seed["crossword"]["clue"],
                               "row": start_r, "col": c, "orientation": "down"})
                used.add(seed["id"])
                done = True
                break
            if done:
                break
    return placed, grid


def main():
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    text = src.read_text() if src and src.exists() else GRAMMAR
    root = parse_grammar(text)
    seeds = []
    walk(root, [], None, [], seeds)
    for s in seeds:
        anchor_branch_points(s)
    build_dendrite_graph(seeds)
    anchors = build_crossword_anchors(seeds)
    grid_entries, grid_cells = build_real_crossword(seeds)
    out = Path("dendritic_seeds")
    out.mkdir(exist_ok=True)
    (out / "seeds.json").write_text(json.dumps(seeds, indent=2))
    (out / "crossword_anchors.json").write_text(json.dumps(anchors, indent=2))
    (out / "grid.json").write_text(json.dumps(
        {"entries": grid_entries,
         "cells": [[r, c, ch] for (r, c), ch in grid_cells.items()]}, indent=2))
    print(f"seeds:              {len(seeds)}")
    print(f"max depth:          {max(s['depth'] for s in seeds)}")
    print(f"crossword anchors:  {len(anchors['by_letter'])} distinct letters")
    print(f"grid entries:       {len(grid_entries)}")
    print(f"grid cells:         {len(grid_cells)}")
    print()
    print("sample seed:")
    print(json.dumps(seeds[5], indent=2)[:900] + "...")


if __name__ == "__main__":
    main()
