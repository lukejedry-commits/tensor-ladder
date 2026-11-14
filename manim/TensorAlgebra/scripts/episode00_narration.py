"""
Episode 0 narration: THE source of truth for the generated voice-over audio.

`scripts/episode00_voiceover.md` stays the human-readable script (what is on
screen + what is said). This file is what actually gets sent to ElevenLabs.
If you change a line here, also change it in the .md so the two stay in sync.

Conventions
-----------
* One entry per beat. A beat = one caption (or one visual moment) in
  episode00.py, which plays it with  `with self.narrate("E00_03_b5"):`.
  Where the .md has two captions under one paragraph, the paragraph is split
  at a sentence boundary into two beats.
* Math is written the way it is said: "v super i", "e sub one",
  "beth, super i, sub j", "beth inverse". Never LaTeX, never symbols.
* Audio tags (Eleven v3): [warmly], [curious], [playfully], [serious],
  [short pause], [laughs softly]...  Kept sparse on purpose: fun, but serious.
  Tags are spoken as direction, not read aloud. Pauses: v3 has no SSML
  <break>; use [short pause], "..." or punctuation.
* Capitals add emphasis in v3 (used once: "NOT v squared").
* PRONUNCIATIONS below is applied (whole words, case-sensitive) just before
  the text is sent, so this file stays readable while single letters are not
  misread (a lone "v" can come out as "five", a lone "e" as "eh").
  Changing a substitution changes the cache key, so affected beats regenerate.
"""

# Applied by voiceover.py right before synthesis (regex whole-word, in order).
PRONUNCIATIONS = {
    "v": "vee",
    "e": "ee",
    "f prime": "eff prime",
    "tilde": "tilda",          # TIL-duh (otherwise often "til-DAY")
    "mu": "myoo",
    "nu": "noo",
    "covector": "co-vector",
    "covectors": "co-vectors",
    "Covectors": "Co-vectors",
}

NARRATION = {
    # ---------------------------------------------------------------- Part 1
    "E00_01_b1": "[warmly] Welcome to Tensors, from the Ground Up. This is Episode Zero: "
                 "the instruction manual for everything that follows.",
    "E00_01_b2": "Here's an arrow. Notice that nothing about it needs a grid. It points somewhere, "
                 "it has a length, and it was here before anyone picked coordinates.",
    "E00_01_b3": "Now pick a basis: these two blue arrows. Measured against them, our arrow becomes "
                 "a pair of numbers... one, three.",
    "E00_01_b4": "Pick a different basis, the coral one, and the very same arrow becomes... two, one.",
    "E00_01_b5": "The arrow never moved. Only the numbers changed. Same arrow, different numbers. "
                 "[short pause] Honestly? That's the whole series, in one sentence.",
    "E00_01_b6": "But before we get there, we need to agree on how to write it all down. "
                 "So: [playfully] the house rules.",

    # ---------------------------------------------------------------- Part 2
    "E00_02_b1": "Rule one. When you see a bold letter, like this bold v, it means an object: "
                 "the arrow itself, not a list of numbers.",
    "E00_02_b2": "Basis vectors are arrows too, so they're bold as well: e sub one, and e sub two.",
    "E00_02_b3": "Now look at the plain letters: v super one and v super two. They're components, "
                 "just numbers. They're the recipe: how much of e sub one, and how much of e sub two, "
                 "it takes to build v.",
    "E00_02_b4": "Here the recipe is one step along e sub one, then three steps along e sub two. "
                 "But these numbers only make sense relative to this basis. Change the basis and the "
                 "recipe changes. The bold arrow doesn't care.",
    "E00_02_b5": "So: bold means object, plain means number. Hold on to that one. "
                 "[knowingly] It'll save you a lot of confusion.",

    # ---------------------------------------------------------------- Part 3
    "E00_03_b1": "Rule two: the height of an index means something. Components of a vector carry "
                 "their index up high. v super i.",
    "E00_03_b2": "Basis vectors carry theirs down low. e sub i.",
    "E00_03_b3": "The letter i is just a label. It can be one or two in the plane, or three once we "
                 "go three D.",
    "E00_03_b4": "And a heads-up for much later: Latin letters like i, j and k count directions in "
                 "space. Greek letters like mu and nu are reserved for spacetime. "
                 "We won't need those for a while.",
    "E00_03_b5": "[serious] Careful, though. An upper index is not an exponent. v super two means "
                 "component number two, NOT v squared.",
    "E00_03_b6": "If we ever do mean a square, you'll see parentheses: v super two, squared. "
                 "No exceptions.",
    "E00_03_b7": "So for vectors, components go up and the basis goes down.",
    "E00_03_b8": "In Part Seven we'll meet covectors, which flip it: components down, basis up. "
                 "Keep this little table in your back pocket.",

    # ---------------------------------------------------------------- Part 4
    "E00_04_b1": "Rule three is a shortcut. Writing out every term like this gets old fast, and it "
                 "only gets worse in three D, or with more indices.",
    "E00_04_b2": "So first we squeeze it into a sum: v equals the sum over i of v super i, e sub i.",
    "E00_04_b3": "And then we drop the sigma altogether. The sum is still happening... "
                 "it's just implied.",
    "E00_04_b4": "How do you know? Look at the index i. It appears twice in the same term, once up "
                 "and once down. That pattern means: sum over it. This is the Einstein summation "
                 "convention, and from here on, it's always on.",
    "E00_04_b5": "Alpha sub i, v super i: one down, one up. That's a sum. You'll see this one a lot.",
    "E00_04_b6": "But v super i, v super i, with both indices up? That's not a sum. On this channel, "
                 "it's a mistake. [playfully] If you ever see one on screen, call me out in the comments.",

    # ---------------------------------------------------------------- Part 5
    "E00_05_b1": "Rule four is about changing your point of view. Here's our vector, written in the "
                 "old, blue basis: v equals v super i, e sub i.",
    "E00_05_b2": "Now we choose a new basis. Anything that belongs to the new basis gets a little "
                 "squiggle on top: a tilde.",
    "E00_05_b3": "The new basis vectors are e tilde sub i, and the new components are v tilde super i.",
    "E00_05_b4": "Put them together. Notice what's missing: the bold v has no tilde. The vector "
                 "doesn't belong to either basis. Only our description of it changes.",
    "E00_05_b5": "Plenty of textbooks use a prime instead: e prime sub i. [short pause] We won't.",
    "E00_05_b6": "Once we get to tensor calculus, a prime starts to look like a derivative, like "
                 "f prime of x. A tilde never does. So: tilde, always.",

    # ---------------------------------------------------------------- Part 6
    "E00_06_b1": "Rule five: meet beth. It's the second letter of the Hebrew alphabet, and it makes "
                 "a \"B\" sound.",
    "E00_06_b2": "B, for basis. [excited] Beth is our change-of-basis matrix. Every time we switch "
                 "bases, beth is the machine that does it.",
    "E00_06_b3": "For our coral basis, beth is this matrix. Read it column by column. The first "
                 "column, one, one, is e tilde sub one, written in the old basis. The second column, "
                 "minus one, one, is e tilde sub two.",
    "E00_06_b4": "Its entries get staggered indices: beth, super i, sub j. The upper index comes "
                 "first and picks the row. The lower one comes second and picks the column. "
                 "The stagger tells you which is which.",
    "E00_06_b5": "Going forward, beth builds the new basis from the old: e tilde sub j equals beth, "
                 "super i, sub j, e sub i. The index i shows up once up and once down, so it's "
                 "summed. The index j is free, and it sits low on both sides, exactly as it should.",
    "E00_06_b6": "[curious] And here's the twist. The components go the other way, with beth "
                 "inverse: v tilde super i equals beth inverse, super i, sub j, v super j. They move "
                 "against the basis. That's where the word contravariant comes from.",
    "E00_06_b7": "Check it with our arrow. Beth inverse takes the old components, one, three, and "
                 "gives two, one: the exact numbers from the cold open. Same arrow, as promised.",
    "E00_06_b8": "We'll derive all of this properly in Episode Two. For today, just learn the names.",

    # ---------------------------------------------------------------- Part 7
    "E00_07_b1": "Rule six: Greek letters, like alpha, gamma and omega, mean covectors. They're "
                 "never bold, so you can't mistake one for a vector.",
    "E00_07_b2": "And we never use beta. [laughs softly] It's far too easy to confuse with beth.",
    "E00_07_b3": "So what is a covector? Picture a stack of evenly spaced lines, with an arrow "
                 "showing which way the value goes up.",
    "E00_07_b4": "Feed it a vector, and it hands you back a number: how many lines the arrow "
                 "crosses. Our arrow crosses one... and lands right on two. So alpha of v is two.",
    "E00_07_b5": "Covectors get their own basis, called the dual basis: epsilon super i, "
                 "with the index up.",
    "E00_07_b6": "Epsilon super one counts steps along e sub one. Epsilon super two counts steps "
                 "along e sub two.",
    "E00_07_b7": "Any covector is a recipe made of those: alpha equals alpha sub i, epsilon super i. "
                 "And notice the heights. The components are down this time, exactly the reverse "
                 "of vectors.",
    "E00_07_b8": "Put a covector and a vector together and the indices pair up, one down and one up, "
                 "so it's a sum. Minus one times one, plus one times three: two. The same number we "
                 "counted from the picture.",

    # ---------------------------------------------------------------- Part 8
    "E00_08_b1": "That's the whole rulebook. Here it is, on one card. Every object has its own "
                 "color, every basis has a bold, vivid color, and components are a paler tint of the "
                 "basis they're measured in. Pause here any time you get lost. "
                 "I'll pin it in the description, too.",
    "E00_08_b2": "Next time, we slow way down and ask a question that sounds too simple to be "
                 "interesting: [curious] what is a vector, really? [warmly] See you there.",
}
