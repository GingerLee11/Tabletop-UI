# CAMPAIGN CONSTANTS:

CAMPAIGN_STATUS = [
    ('Open', "Open"),
    ('Full', "Full"),
    ('Completed', "Completed"),
]

CHARACTERS = [
    ('The Blessed', 'The Blessed'),
    ('The Fox', 'The Fox'),
    ('The Heavy', 'The Heavy'),
    ('The Judge', 'The Judge'),
    ('The Lightbearer', 'The Lightbearer'),
    ('The Marshal', 'The Marshal'),
    ('The Ranger', 'The Ranger'),
    ('The Seeker', 'The Seeker'),
    ('The Would-Be Hero', 'The Would-Be Hero'),
]

BLESSED_STARTING_MOVES = [
    'SPIRIT TONGUE',
    'CALL THE SPIRITS',
]

BLESSED_BACKGROUND_MOVES = {
    'INITIATE': 'RITES OF THE LAND',
    'RAISED BY WOLVES': 'TRACKLESS STEP',
    'VESSEL': "DANU'S GRASP",
}

# There are no starting moves
# for The Fox

HEAVY_STARTING_MOVES = [
    'DANGEROUS',
    'HARD TO KILL',
]

JUDGE_STARTING_MOVES = [
    'CENSURE',
    'CHRONICLER OF STONETOP',
]
LIGHTBEARER_STARTING_MOVES = [
    'CONSECRATED FLAME',
    'INVOKE THE SUN GOD',
]

MARSHAL_STARTING_MOVES = [
    'CREW',
    'LOGISTICS',
]

MARSHAL_BACKGROUND_MOVES = {
    'LUMINARY': 'WE HAPPY FEW',
    'RAISED BY WOLVES': 'TRACKLESS STEP',
    'SCION': "VETERAN CREW",
}
MARSHAL_CREW_TAGS = [
    'archers',
    'athletic',
    'brave',
    'cunning',
    'devoted',
    'group',
    'hardy',
    'intimidating',
    'observant',
    'patient',
    'respected',
    'stealthy',
    'warriors',
]

COMPLEXITY_CHOICES = [
    ('low complexity', 'low complexity'),
    ('low/medium complexity', 'low/medium complexity'),
    ('medium complexity', 'medium complexity'),
    ('high complexity', 'high complexity'),
    ('variable complexity', 'variable complexity'),
]

DAMAGE_DIE = [
    ('D4', 'D4'),
    ('D6', 'D6'),
    ('D8', 'D8'),
    ('D10', 'D10'),
    ('D12', 'D12'),
    ('D20', 'D20'),
]

PHYSICAL_CHARACTERISTIC = [
    ("appearance1", "appearance1"),
    ("appearance2", "appearance2"),
    ("appearance3", "appearance3"),
    ("appearance4", "appearance4"),
]

# CHARACTER CONSTANTS:

POUCH_ORIGINS = [
    ("an heirloom", "an heirloom"),
    ("made just for you", "made just for you"),
    ("your own work", "your own work"),
]

POUCH_MATERIAL = [
    ("fur","fur"),
    ("drakescale","drakescale"),
    ("leather","leather"),
    ("woven","woven"),
    ("demonflesh","demonflesh"),
]

POUCH_AESTHETICS = [
    ("unadorned","unadorned"),
    ("beadwork","beadwork"),
    ("rich dyes","rich dyes"),
    ("runes","runes"),
]

STOCK_TYPE = [
    ('tag', 'tag'),
    ('move', 'move'),
]

DANU_SHRINE = [
    ("loved, well-used, dripping with offerings and petitions.", "Loved, well-used, dripping with offerings and petitions."),
    ("little more than a token of respect, for her holy places are anywhere but here.", "Little more than a token of respect, for her holy places are anywhere but here."),
    ("given a wide berth by most, and approached only with care and propitiation.", "Given a wide berth by most, and approached only with care and propitiation."),
    ("neglected and all but forgotten, except by a few.", "Neglected and all but forgotten, except by a few."),
]

SHRINE_OF_ARATIS = [
    ("a hub of the community, a place of frequent rites, petitions, and celebrations", "A hub of the community, a place of frequent rites, petitions, and celebrations"),
    ("used only on high holidays, for each home keeps its own shrine above the hearth", "Used only on high holidays, for each home keeps its own shrine above the hearth"),
    ("neglected by most, tended only by you and a handful of believers", "Neglected by most, tended only by you and a handful of believers"),
    ("a grim place of judgement and punishment, shunned by all but her chosen", "A grim place of judgement and punishment, shunned by all but her chosen"),
    ("newly established, cramped and spare", "Newly established, cramped and spare"),
]

DETAIL_TYPE = [
    ("theme", "There was that time that you..."),
    ("middle", "And you ended up..."),
    ("results", "But all you've got left to show for it is..."),
]

TALE_OPENING = [
    ("got lost in the Great Wood", "got lost in the Great Wood"),
    ("got lost in the Flats", "got lost in the Flats"),
    ("got lost in the Stepland", "got lost in the Steplands"),
    ("got lost in Ferrier's Fen", "got lost in Ferrier's Fen"),
    ("got lost in foothills", "got lost in the foothills"),
    ("got lost in the hufel peaks", "got lost in the hufel peaks"),
    ("were on watch when the crinwin raided", "were on watch when the crinwin raided"),
    ("dared each other to explore the Ruined Tower", "dared each other to explore the Ruined Tower"),
    ("managed to rile up a small band of Hillfolk", "managed to rile up a small band of Hillfolk"),
    ("braved the Labyrinth, just a little", "braved the Labyrinth, just a little"),
    ("stole that crazy old man's book", "stole that crazy old man's book"),
    ("went poking around the old Barrow Mounds", "went poking around the old Barrow Mounds"),
]

TALE_ENDINGS = [
    ("a story no one believes.", "a story no one believes."),
    ("a nasty scar; wanna see?", "a nasty scar; wanna see?"),
    ("the occasional nightmare.", "the occasional nightmare."),
    ("this map with runes no one can read.", "this map with runes no one can read."),
    ("this key that open who-knows-what.", "this key that open who-knows-what."),
]

HISTORIES_OF_VIOLENCE = [
    ("stories of glory", "Just about everyone here talks about the time you..."),
    ("terrible stories", "But folks are less keen to discuss..."),
    ("fears", "What keep you up at night?"),
]

CHRONICAL = [
    ("positive", "On the plus side, it..."),
    ("negative", "But alas it..."),
]

WORSHIP_OF_HELIOR = [
    ("ancient, widespread, and well-known", "ancient, widespread, and well-known"),
    ("most common in Lygos and the south", "most common in Lygos and the south"),
    ("a new thing, still unheard of by many", "a new thing, still unheard of by many"),
    ("widely persecuted", "widely persecuted"),
]

HELIORS_SHRINE = [
    ("the place of highest honor, even if Tor is more popular", "the place of highest honor, even if Tor is more popular"),
    ("been well-tended and given due respect", "been well-tended and given due respect"),
    ("recently been restored, perhaps by you", "recently been restored, perhaps by you"),
    ("seen better days for certain", "seen better days for certain"),
]

LIGHTBEARER_POWER_ORIGINS = [
    ("through years of study and devotion", "through years of study and devotion"),
    ("when your predecessor passed them on", "when your predecessor passed them on"),
    ("suddenly, at a moment of great need.", "suddenly, at a moment of great need."),
    ("after a visitation from Helior or one of his servants", "after a visitation from Helior or one of his servants"),
    ("when you first laid eyes upon the _______", "when you first laid eyes upon the _______"),
]

WAR_STORIES = [
    ("to repel a nighttime raid by crinwin from the Great Wood.", "to repel a nighttime raid by crinwin from the Great Wood."),
    ("to drive off bandits who'd taken up near the Ruined Tower", "to drive off bandits who'd taken up near the Ruined Tower"),
    ("to fend off Hillfolk pursuing a blood feud", "to fend off Hillfolk pursuing a blood feud"),
    ("against Brennan and his Claws, before they settled in Marshedge.", "against Brennan and his Claws, before they settled in Marshedge."),
    ("to face a brutish hagr, come down from the Foothills to wreak havoc.", "to face a brutish hagr, come down from the Foothills to wreak havoc."),
    ("to hunt down beasts (wolves, drakes, or bears maybe?) who'd been preying on the village.", "to hunt down beasts (wolves, drakes, or bears maybe?) who'd been preying on the village."),
]

SOMETHING_WICKED = [
    ("A dark, unwholesome presence lurking in the Great Wood", "A dark, unwholesome presence lurking in the Great Wood"),
    ("A strange, furtive figure seen near the Ruined Tower", "A strange, furtive figure seen near the Ruined Tower"),
    ("Something big & savage stalking the northern foothills", "Something big & savage stalking the northern foothills"),
    ("Whatever's made the lizard-like ganagoeg of Ferrier's Fen so bold", "Whatever's made the lizard-like ganagoeg of Ferrier's Fen so bold"),
    ("That of which the Hillfolk refuse to speak", "That of which the Hillfolk refuse to speak"),
]

WAR_STORY_QUESTIONS = [
    ("When exactly did it happen?", "When exactly did it happen?"),
    ("Who lost their life, and who mourns them?", "Who lost their life, and who mourns them?"),
    ("Who from Stonetop was mainmed, and how?", "Who from Stonetop was mainmed, and how?"),
    ("Who saved the day, and how?", "Who saved the day, and how?"),
    ("How did the enemy get away, and whom do you still blame for it?", "How did the enemy get away, and whom do you still blame for it?"),
    ("Who comported themselves with honor?", "Who comported themselves with honor?"),
    ("What's been bugging you about it ever since?", "What's been bugging you about it ever since?"),
    ("What's got you even more worried now?", "What's got you even more worried now?"),
]

MAJOR_ARCANA_QUESTIONS = [
    ("Where did you aquire it?", "Where did you aquire it?"),
    ("From whose grasp did you wrest it?", "From whose grasp did you wrest it?"),
    ("Who else wants it?", "Who else wants it?"),
    ("What did it cost you?", "What did it cost you?"),
]

TERRIBLE_PURPOSE = [
    ("A loved one was killed or abducted", "A loved one was killed or abducted"),
    ("Someone gave their life to save you", "Someone gave their life to save you"),
    ("Your idol sacrificed themselves to save many", "Your idol sacrificed themselves to save many"),
    ("You stumbled upon a dark mystery", "You stumbled upon a dark mystery"),
    ("You must make amends for a terrible mistake", "You must make amends for a terrible mistake"),
]

FEAR_AND_ANGER = [
    ("fear", "fear"),
    ("anger", "anger"),
]

PRONOUNS = [
    ("he/him", "he/him"),
    ("she/her", "she/her"),
    ("they/them", "they/them"),
]

AMMO_CHOICES = [
    ('full', 'full'),
    ('plenty left', 'plenty left'),
    ('low ammo', 'low ammo'),
    ('all out', 'all out'),
]

# NPC CONSTANTS:

NPC_TYPE = [
    ("Initiate of Danu", "Initiate of Danu"),
]

INITIATES_OF_DNAU = [
    ("Enfys", "Enfys"),
    ("Olwin", "Olwin"),
    ("Afon", "Afon"),
    ("Gwendyl", "Gwendyl"),
    ("Seren the Eldest", "Seren the Eldest"),
]

STONETOP_RESIDENCES = [
    ("Barrier Pass", "Barrier Pass"),
    ("Stonetop", "Stonetop"),
    ("Marshedge", "Marshedge"),
    ("Gordin's Delve", "Gordin's Delve"),
    ("The Steplands", "The Steplands"),
    ("The Manmarch", "The Manmarch"),
    ("Lygos (and other points south)", "Lygos (and other points south)"),
]

CREW_INSTINCTS = [
    ('To bicker, infight, and hold grudges', 'To bicker, infight, and hold grudges'),
    ('To hew to tradition and superstition', 'To hew to tradition and superstition'),
    ('To indulge their baser instincts', 'To indulge their baser instincts'),
    ('To lord over others', 'To lord over others'),
    ('To take needless risks', 'To take needless risks'),
    ('To take things too far', 'To take things too far'),
]

CREW_COSTS = [
    ('Merry-making, as a group', 'Merry-making, as a group'),
    ('Public recognition and respect, honor', 'Public recognition and respect, honor'),
    ('Risks taken, by you, to help them', 'Risks taken, by you, to help them'),
    ('Victories won against worthy foes', 'Victories won against worthy foes'),
    ('Wealth gained for themselves or Stonetop', 'Wealth gained for themselves or Stonetop'),
]

ANIMAL_COMPANION_INSTINCTS = [

    ('To bully and threaten', 'To bully and threaten'),
    ('To fill its belly', 'To fill its belly'),
    ('To get distracted', 'To get distracted'),
    ('To give chase', 'To give chase'),
    ('To make mischief', 'To make mischief'),
    ('To startle and panic', 'To startle and panic'),
    ('To run rampant', 'To run rampant'),
]

ANIMAL_COMPANION_COSTS = [

    ('Play, grooming, training, affection', 'Play, grooming, training, affection'),
    ('Time off on its own, free to roam', 'Time off on its own, free to roam'),
    ('Cozy quarters, comform, ample food', 'Cozy quarters, comform, ample food'),
]