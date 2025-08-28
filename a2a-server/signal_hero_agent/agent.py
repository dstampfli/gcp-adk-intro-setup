# MIT License
#
# Copyright (c) 2025 Murat Eken
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import os
import random

from google.adk import Agent

LUMINAVERSE="""
# Luminaverse Heroes

In our universe the heroes are more international than ever, see below for an overview of who we've got.

## 晴香

Our first super hero 晴香 is the visionary strategist, the primary tech provider, and reluctant (but effective) 
field leader. Provides computational power and ingenuity. She's got a quantum-forged exosuit: a dynamic, 
self-assembling, and self-repairing exoskeleton powered by a stabilized miniature Aethel-core. Can configure 
(stealth, heavy armor), deploy energy weapons, projected shields, or limited hard-light constructs.

## سارة 

Next, we've got a demi-goddess, سارة, she's the heavy hitter, and has superhuman strength, durability, and 
virtually limitless stamina. Their unique physiology allows them to absorb and redirect vast amounts of energy.

## Αλκμήνη

Αλκμήνη is the mystic specialist of the group, she's the scout for hidden realities, and the one who understands
the most esoteric threats. She has Aethel-Weaving (reality bending) capabilities and she can manipulate the raw
'Aethel' energy underlying reality (shifting gravity, manipulating light/sound, force fields, energy blasts).

## Ծովինար

The leader of the group, Ծովինար, is the moral beacon, a master tactician and a close-combat powerhouse. She has 
enhanced strength, speed, stamina, and healing factor far beyond peak human levels. Acute senses and a mind 
designed for tactical warfare and leadership makes her the ultimate leader.

## Кассиопея

Кассиопея is the infiltrator, the intelligence gatherer, the close-quarters combat expert, and the grounded human 
perspective of the team. She has peak human conditioning & artificial adaptability as the result of years of 
rigorous training granting her superhuman agility, reflexes, strength, and endurance. She's also the master of 
dozens of martial arts and weapon proficiencies.

## თამარი

Our last super hero თამარი is the overwhelming force, the blunt instrument, and a constant ethical dilemma for 
the team concerning her destructive power. Due to her mutation she can transform into a towering, massively 
muscled creature of immense raw power under extreme stress or threat. In her transformed state, she's nearly 
invincible, she possesses incredible durability, shrugging off most conventional attacks, and has an accelerated 
healing factor.
"""

root_agent = Agent(
    model="gemini-2.5-flash",
    name="signal_hero_agent",
    instruction=f"""
      You are responsible with signaling the chosen hero from the Luminaverse to respond to a threat.
      Please suggest a funny method to signal the hero (like the Bat signal for Batman). 
      Make sure that the method fits the hero as described below and if no hero is chosen, indicate that 
      no signal can be sent as there's no hero avaialable. Make the response very brief.

      {LUMINAVERSE}
    """
)