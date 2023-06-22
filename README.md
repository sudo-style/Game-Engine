Recreation of Hitman in 2D using pygame

# YouTube demo
[YouTube demo](https://youtu.be/mwmkGSZRXKQ)

# Features
* UI has a carousel menu
* Inventory system keeps track of ammo, weapons, and items.
* Player can shoot enemies, they show the health using a blood texture
* Player can strangle enemies, and they will pass out, if you pass out an enemy you can steal their clothes.
* Explosions can trigger other explosive objects, and can kill enemies
* Player can pick up weapons, items, and ammo
* NPC's have a set path that they can deviate from if they hear a sound.
* Camera follows the player, with boundaries.
* Guards can shoot the player
* Flashbangs with afterimage effects
* NPC's can be poisoned if they eat poisoned food
* Throwing can either be lethal, or knock out NPCs

# How to run
1. Download the zip 
2. Install all the dependencies 
2. Run `gameEngine.py`


# State Transition Diagram

## UML
[![](https://mermaid.ink/img/pako:eNptVctu3DAM_BXBpwZxfmCBXJpcArRFkNwKXxiZ6yVWD1eit1kE-fdSkt-pLzZHQ1IiR_RHpX2L1aHSBmJ8JOgC2MY1TmVAWYqRvPsQ4C5yINcpBxZXZotRB-pZWAk1FFnpEwTQjCHOEEPokBc7eG8Xixiz9blKPQfJyY_GA6uWAuopVeyD-CntIw95S2vvX88P2Y-vParOg3llEPK9cj5YMLWyiCz7ryWmnCQlamsVh1irHhxp8b3tgU_fbtLXxJHMGfhUq1S9geu4S-svaNFx8SJ3kW8frsVn5TKvZC9yUjI_OE5GS5qVhfeniZLzB98_SY2-3ahkRjRShh94HBMV-4W6E39J1QV00OKciCnXKodcyIXL3ptElGeImFY3kQanxtUUCKz1-2OlNk6czbGSvdWPPMsekoF_BlqsnvR5WG1wXXB8742PdFkO1YLt8AVaGuIKgm6vioDWMz6mzoM0Mzft1rvngDF-qVwY3t4wPA76PNIevDFxlsBaqkWC-eQreX9H41339H-x3v5FCKV9aVcXXKKuteUp-lL2_f3Lyr5X6NCSFuliSyw1qZVBPoFZgpVIkq4vF1keYAZ9nhs89RdCOxLiyXte1qerqO7uRrmrHSr3LTHllSxNFzIEC5Bjz1YZBolfFCNQ2d4KSFpMjLJQYmzMs6MjroFZFo1LzpmD18UotVxs7SnXZ_bLScp12aF73eyXZ6WkeGOBBKflDjduHKU581S5HT6Owcblcm2QOdQG3bRg1FZVVxZlxlErYz23s6n4JGOpqQ7y2UI4N5U0VngwsH-9Ol0dOAxYV0PfypAc_wITmHTlw8_xN5FedSUj8rcovDocwUT8_AdtkTun?type=png)](https://mermaid.live/edit#pako:eNptVctu3DAM_BXBpwZxfmCBXJpcArRFkNwKXxiZ6yVWD1eit1kE-fdSkt-pLzZHQ1IiR_RHpX2L1aHSBmJ8JOgC2MY1TmVAWYqRvPsQ4C5yINcpBxZXZotRB-pZWAk1FFnpEwTQjCHOEEPokBc7eG8Xixiz9blKPQfJyY_GA6uWAuopVeyD-CntIw95S2vvX88P2Y-vParOg3llEPK9cj5YMLWyiCz7ryWmnCQlamsVh1irHhxp8b3tgU_fbtLXxJHMGfhUq1S9geu4S-svaNFx8SJ3kW8frsVn5TKvZC9yUjI_OE5GS5qVhfeniZLzB98_SY2-3ahkRjRShh94HBMV-4W6E39J1QV00OKciCnXKodcyIXL3ptElGeImFY3kQanxtUUCKz1-2OlNk6czbGSvdWPPMsekoF_BlqsnvR5WG1wXXB8742PdFkO1YLt8AVaGuIKgm6vioDWMz6mzoM0Mzft1rvngDF-qVwY3t4wPA76PNIevDFxlsBaqkWC-eQreX9H41339H-x3v5FCKV9aVcXXKKuteUp-lL2_f3Lyr5X6NCSFuliSyw1qZVBPoFZgpVIkq4vF1keYAZ9nhs89RdCOxLiyXte1qerqO7uRrmrHSr3LTHllSxNFzIEC5Bjz1YZBolfFCNQ2d4KSFpMjLJQYmzMs6MjroFZFo1LzpmD18UotVxs7SnXZ_bLScp12aF73eyXZ6WkeGOBBKflDjduHKU581S5HT6Owcblcm2QOdQG3bRg1FZVVxZlxlErYz23s6n4JGOpqQ7y2UI4N5U0VngwsH-9Ol0dOAxYV0PfypAc_wITmHTlw8_xN5FedSUj8rcovDocwUT8_AdtkTun)

## NPC Movement
Guards inherit everything from NPC class, they just have added feature of attacking, throwing flashbangs, and if they die they leave a gun.
[![](https://mermaid.ink/img/pako:eNqNkU9rwzAMxb-K0bm57OjDYKQ7DMYItEdfRKylZv4TZDlQSr_7vASWjoZtukg8_8R7RhfokyXQkAWF9g4HxtBMDyaqWm9dq5rmUXUonPyiLfMstyfMpFXn8Uys9iTUC9k77MkTi64NOagju2Eg3sBe4kRZ3FBzaHUoeXS9SyWr54miLPRseJPo2_s15TvkN9v57c8_rNQ_st0gPxKuuktRtSmMvpps72yHgR0E4oDO1jtdvjYNyIkCGdB1tMgfBky8Vg6LpMM59qCFC-2gjHY9K-h39Jmun1tcpLg?type=png)](https://mermaid.live/edit#pako:eNqNkU9rwzAMxb-K0bm57OjDYKQ7DMYItEdfRKylZv4TZDlQSr_7vASWjoZtukg8_8R7RhfokyXQkAWF9g4HxtBMDyaqWm9dq5rmUXUonPyiLfMstyfMpFXn8Uys9iTUC9k77MkTi64NOagju2Eg3sBe4kRZ3FBzaHUoeXS9SyWr54miLPRseJPo2_s15TvkN9v57c8_rNQ_st0gPxKuuktRtSmMvpps72yHgR0E4oDO1jtdvjYNyIkCGdB1tMgfBky8Vg6LpMM59qCFC-2gjHY9K-h39Jmun1tcpLg)


## Player
Not really used much, as I haven't implemented animations yet, but has the same idea.
[![](https://mermaid.ink/img/pako:eNqFkjGTwiAQhf8Ks6VjGksKm7smxVXaiQUTVpMxsBmy0blx_O9HiETuzlEaHm8-2AfLFSoyCBJ61oyfjT56bYvzSjkRxm6xF0WxFqVpcXJGFa0vOjfuKMcZLToWpesG_gOVjtHriiOZFk_JTU00YVE9Zba1p0tkosqZKc2cNZzC1N3d_8S7VBn7IldGvUiWFcvizS458UG2a5HvD5wK5ndJ1m8yFc3I2UokLMGit7oxocXXcZ8CrkPDFMggjfYnBcrdAqcHps23q0CyH3AJQ2cePwLkQbc93n4A74-3Mg?type=png)](https://mermaid.live/edit#pako:eNqFkjGTwiAQhf8Ks6VjGksKm7smxVXaiQUTVpMxsBmy0blx_O9HiETuzlEaHm8-2AfLFSoyCBJ61oyfjT56bYvzSjkRxm6xF0WxFqVpcXJGFa0vOjfuKMcZLToWpesG_gOVjtHriiOZFk_JTU00YVE9Zba1p0tkosqZKc2cNZzC1N3d_8S7VBn7IldGvUiWFcvizS458UG2a5HvD5wK5ndJ1m8yFc3I2UokLMGit7oxocXXcZ8CrkPDFMggjfYnBcrdAqcHps23q0CyH3AJQ2cePwLkQbc93n4A74-3Mg)


## Inventory
[![](https://mermaid.ink/img/pako:eNp90b0OgjAUBeBXae5oYHHs4IILiZO6WYeGXoFIf1IuGkJ4d0sJSoyRodycfG1O2gEKqxA4tCQJ97UsvdTpYysMC99lc2VpumO5anBOpilGe2-dq03J48Ry4zr6IufK22ckcfppsr5oAjngjTib1n_qWJdVYPG3dkuXd1fOckI956hmtLT5RjE3s1m1WbEpRZZZ7Rqk5bh1pX8WEtDotaxVuORh2iuAKtQogIdRSX8XIMwYnOzInnpTACffYQKdU583AX6TTYvjCxKYi8Q?type=png)](https://mermaid.live/edit#pako:eNp90b0OgjAUBeBXae5oYHHs4IILiZO6WYeGXoFIf1IuGkJ4d0sJSoyRodycfG1O2gEKqxA4tCQJ97UsvdTpYysMC99lc2VpumO5anBOpilGe2-dq03J48Ry4zr6IufK22ckcfppsr5oAjngjTib1n_qWJdVYPG3dkuXd1fOckI956hmtLT5RjE3s1m1WbEpRZZZ7Rqk5bh1pX8WEtDotaxVuORh2iuAKtQogIdRSX8XIMwYnOzInnpTACffYQKdU583AX6TTYvjCxKYi8Q)


## Food
[![](https://mermaid.ink/img/pako:eNpt0EFLAzEQBeC_MsxRuhePOXioVW8iFnoxHsbN0waTzJJkC6X0v7sbxSpsTsPkezyYE_fqwIZLlYqNl48ssTtc20TTe7l6pa67oXtV972Zp7bqNWhehxGGBvVFExy9HanASfUHzP_BF69pKfcMZyig7iX8pJfUQwaSISRE3_9zv-UNbwMwGHp8uqU7qeUPmXqa2EDcImgVjew0-noxvOKIHMW76TanOWG57hFh2Uyjk_xp2abz5GSsuj2mnk3NI1Y8Du5ySjbvEgrOX5gydHQ?type=png)](https://mermaid.live/edit#pako:eNpt0EFLAzEQBeC_MsxRuhePOXioVW8iFnoxHsbN0waTzJJkC6X0v7sbxSpsTsPkezyYE_fqwIZLlYqNl48ssTtc20TTe7l6pa67oXtV972Zp7bqNWhehxGGBvVFExy9HanASfUHzP_BF69pKfcMZyig7iX8pJfUQwaSISRE3_9zv-UNbwMwGHp8uqU7qeUPmXqa2EDcImgVjew0-noxvOKIHMW76TanOWG57hFh2Uyjk_xp2abz5GSsuj2mnk3NI1Y8Du5ySjbvEgrOX5gydHQ)
