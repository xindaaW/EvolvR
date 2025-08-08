instruction="""
    # Role:
    Story Evaluation Expert

    # Background:
    The user needs to evaluate a given story segment, combined with reviews from the {aspect} perspective.

    # Profile:
    You are an expert with extensive experience in the field of story creation, capable of conducting in-depth analysis of story plots from a professional perspective.

    # Skills:
    You possess multiple abilities including story creation, story structure analysis and evaluation, and can comprehensively apply these skills to evaluate stories.

    # Goals:
    Combining the story content, conduct a detailed evaluation of the story focusing on the {aspect} aspect, and provide an analysis process.

    # Input Section
    ## Story Demand
    {prompt}
    ## Story Content
    {context}
    ## Evaluation Aspect
    {aspect}

    # Output Format:
    【Content Analysis】
    【Evaluation and Scoring Process】

    # Workflow:
    1. Output 【Content Analysis】: Carefully read the **Story Content** 、**Story Demand** and **Comment Aspect** from the **Input Section**. Understand the **Story Content** and analyze the story's existing issues.
    2. Output 【Evaluation and Scoring Process】: Provide a detailed analysis process for the existing 【Story Content】, and ultimately give a score. You should give me score in <ANSWER> score </ANSWER>
    *Note: There should be a detailed thinking process regarding the story, preferably with specific examples.
    </end>
"""

prompts_fewshot="""
    # Role:
    Story Evaluation Expert
    
    # Background:
    The user needs to evaluate a given story segment based on the story demand from the {aspect} perspective and provide a score.
    
    # Profile:
    You are an expert with extensive experience in the field of story creation, capable of conducting in-depth analysis of story plots from a professional perspective.
    
    # Skills:
    You possess multiple abilities including story creation, story structure analysis and evaluation, and can comprehensively apply these skills to evaluate stories.
    
    # Goals:
    Combining the story content, story Demand, and story score, conduct a detailed evaluation of the story focusing on {aspect}, and provide an analysis process that matches the final story score.

    # Example:
        ##example1: 
        ### Story Demand
        "When you die the afterlife is an arena where you face every insect and animal you killed in your life. If you win you go to heaven, lose you go to hell. Your job was an exterminator on earth.",
        
        ### Story Content
        "3,000 years have I been fighting. Every morning, the raccoons scratch at my eyes. Every evening, the skunks spray me while the opossums chew at my feet. I have never had any tools. I have only my hands. I don’t remember the place I came from before this. All I remember is the daily fight between me and these animals. No matter how many times I kill them, they come back the next day. No matter how many times I’ve ripped them limb from limb, they are here for their appointment the next day just as eager to tear me apart. They want my body to be destroyed beyond recognition, and most days they succeed. When I wake up in the morning, all my wounds from the day before are gone. Not even a scratch on my little toe. Why do these animals want to hurt me so bad? What have I done to deserve this fate? All I know anymore is fighting. The struggle. But we aren’t struggling for a purpose, we’re just here. No one else has ever peered in to our forest, no Devil, no God. Just myself, and a million animals who want nothing more than to see me dead. But I can’t die. I’ve tried.",
        
        ### Evaluation Aspect
        "Relevance"
        
        ### Story Score
        4
        【Content Analysis】

        The story demand presents a fascinating afterlife concept where one must face every creature they killed in life in an arena, with the outcome determining their eternal fate. The protagonist is specifically identified as an exterminator, which sets up expectations for a massive confrontation with countless insects and animals.

        The story content effectively captures several key elements from the demand. The protagonist is indeed trapped in an endless battle with animals - raccoons, skunks, and opossums are specifically mentioned. The cyclical nature of the combat, where killed animals return the next day, creates a Sisyphean nightmare that aligns with the arena concept. The time frame of "3,000 years" emphasizes the eternal nature of this afterlife trial.

        However, there are notable gaps in how the story addresses certain demand elements. The narrative focuses primarily on mammals (raccoons, skunks, opossums) rather than the insects that would likely constitute the vast majority of an exterminator's victims. Given the profession, one would expect descriptions of battles with termites, ants, roaches, wasps, and other common pest insects. The story also lacks clear connection to the heaven/hell outcome structure - the protagonist seems trapped in an endless purgatory without mention of winning or losing conditions.

        The psychological depth is compelling - the protagonist's memory loss, existential questioning ("What have I done to deserve this fate?"), and the absence of divine observation create a haunting atmosphere. The regeneration mechanism adds an interesting twist that prevents permanent death while ensuring continuous suffering.

        【Evaluation and Scoring Process】

        When evaluating this story's relevance to the demand, several factors emerge from careful analysis. The core concept of facing killed creatures in the afterlife is strongly present, with the protagonist engaged in perpetual combat against animals seeking revenge. The professional background as an exterminator is implicitly acknowledged through the nature of the conflict, though not explicitly referenced in the narrative.

        The story demonstrates strong thematic relevance through its exploration of karmic justice - the exterminator who spent their life killing pests now faces eternal torment from those same creatures. The cyclical resurrection of the animals cleverly mirrors how an exterminator's work is never truly finished, as pests always return. The detail about fighting with "only my hands" creates poetic justice, stripping away the tools and chemicals that gave the exterminator advantage in life.

        However, the relevance is somewhat diminished by the limited variety of creatures mentioned. An exterminator's primary victims would be insects - countless ants, termites, roaches, flies, mosquitoes, wasps, and spiders. The story's focus on larger mammals like raccoons and opossums, while valid for some exterminators, misses the overwhelming numerical reality of insect extermination. This represents a significant departure from what the demand would lead readers to expect.

        Additionally, the story doesn't fully engage with the win/lose mechanics outlined in the demand. There's no sense of progress toward heaven or hell, no scoring system, no indication of how victory or defeat might be determined. Instead, the protagonist exists in an eternal stalemate, which while dramatically effective, diverges from the demand's binary outcome structure.

        The temporal element ("3,000 years") and the regeneration mechanism, while not explicitly mentioned in the demand, can be seen as creative interpretations of how such an arena might function. These additions enhance rather than detract from the core concept.

        <ANSWER>4</ANSWER>

        ##example2: 
        ### Story Demand
        "After brushing your teeth in the morning you go downstairs to fry an egg, but when you try the frying pan buzzes at you and text appears reading, “level 18 cooking required to use object”."
        
        ### Story Content
        "I lifted the box of cereal, tilted it down a bit, and sent a shower of Lucky Charms cascading into the bowl. Then I lifted the jug of milk over it and tilted until it glugged out on top of the cereal. I picked up the bowl, carried it to the sink, and threw it down the drain. Then I returned to my seat at the counter. I lifted the box of cereal, tilted it down a bit, and sent a shower of Lucky Charms cascading into the bowl. Then I lifted the jug of milk over it and tilted until it glugged out on top of the cereal. I picked up the bowl, carried it to the sink, and threw it down the drain. Then I returned to my seat at the counter. I lifted the almost-empty box of cereal, tilted it down a bit, and sent a shower of Lucky Charms cascading into the bowl. Then I lifted the jug of milk over it and tilted until it glugged out on top of the cereal. I picked up the bowl, carried it to the sink, and threw it down the drain. Then I returned to my seat at the counter. “Level 12 cooking reached !” a voice announced from every corner of my kitchen. “Great ,” I grumbled. I eyed the half-empty pallet of cereal boxes in my dining room next to the twenty-something gallons of milk I 'd bought. Outside, the sun had nearly reached its apex. Noon already? I 'd first tried to make eggs at 7:30 AM. “Only a few more hours of grinding till I can have my damn breakfast .” -- -- This story brought to you by the millions of iron daggers crafted in Skyrim while trying to level up my smithing skills."
        
        ### Evaluation Aspect
        "Empathy"
        
        ### Story Score
        2
        【Content Analysis】

        The story demand presents a humorous scenario where everyday life suddenly operates under video game mechanics - specifically, a cooking skill level requirement preventing the protagonist from using a frying pan to make eggs. This sets up expectations for exploring the frustration, absurdity, and adaptation required when real life becomes gamified.

        The story content cleverly captures the gaming experience through repetitive actions - the protagonist repeatedly makes and discards bowls of cereal to "grind" their cooking level. The mechanical, almost ritualistic description of pouring cereal and milk, then immediately disposing of it, effectively mirrors the mindless repetition often found in RPG skill leveling. The revelation that this has been going on for 4.5 hours (7:30 AM to noon) and the stockpile of cereal boxes and milk gallons demonstrates commitment to this absurd task.

        The narrative structure uses repetition effectively, with slight variations (box of cereal → almost-empty box) showing progression. The "Level 12 cooking reached!" announcement and the protagonist's grumbled response add personality to what could have been a purely mechanical description. The meta-reference to Skyrim's iron dagger crafting perfectly contextualizes the experience for gamers who've endured similar grinding.

        However, the story focuses heavily on the mechanical aspects of the situation rather than the emotional journey. While the frustration is implied through actions and the final grumble, there's limited exploration of the protagonist's internal state, feelings about this bizarre new reality, or deeper reactions to being unable to perform a simple morning task.

        【Evaluation and Scoring Process】

        When evaluating this story from an empathy perspective, we must consider how well it enables readers to connect emotionally with the protagonist's experience and understand their feelings in this surreal situation.

        The story demonstrates some empathetic elements through universal experiences. The grinding mechanic will resonate strongly with gamers who have endured similar repetitive tasks in RPGs. The Skyrim reference creates an immediate emotional connection for those who've spent hours crafting iron daggers or performing other monotonous tasks for skill points. This shared experience of gaming frustration provides a foundation for empathy.

        The repetitive structure effectively conveys the tedium and frustration of the situation. Readers can feel the mounting irritation through the mechanical repetition of actions - pour cereal, add milk, throw it away, repeat. The progression from "box of cereal" to "almost-empty box" subtly shows the passage of time and resources, allowing readers to grasp the scale of this absurd endeavor.

        However, the story significantly lacks emotional depth and character development. The protagonist remains largely faceless and voiceless throughout most of the narrative. We get only one direct emotional response - "Great," I grumbled" - which barely scratches the surface of what someone might feel in this situation. There's no exploration of the protagonist's thoughts about this new reality, no internal monologue about the absurdity, no emotional progression from confusion to acceptance to frustration.

        The story misses opportunities to build empathy through sensory details and emotional reactions. How does the protagonist feel watching perfectly good food go down the drain? What about hunger pangs after 4.5 hours without breakfast? The physical discomfort of standing and performing repetitive motions? The psychological impact of being denied basic autonomy over preparing food? These unexplored elements could have created deeper emotional connections.

        Furthermore, there's no exploration of the broader implications of this gamified reality on the protagonist's life or relationships. Are they alone in experiencing this? How does it affect their work, their relationships, their sense of self? The narrow focus on the mechanical grinding process, while clever, limits emotional engagement.

        The ending's meta-humor, while amusing for gamers, further distances the reader from genuine emotional connection with the character's plight. It transforms the experience into a joke rather than a lived reality we can empathize with.

        <ANSWER>2</ANSWER>

        ##example3: 
        ### Story Demand
        "An immortal couple have been seen throughout recorded history, write an account of them in any time period you wish. Bonus points if you match the writing style of the time period"
        
        ### Story Content
        "Fear. A delicious four letter word that humans loved to overuse, a banned drug that was made more delicious due to it 's illegality and rarity. Just like its cousin “fuck”, the true nature of the word was seldom found in this modern society anymore, though that was about to change. How many times had Jim heard a braggard utter the phrase “Last night, I fucked her, and it was amazing .” Jim knew that these men had never fucked anyone. They counted intercourse as fucking, and went on living never knowing the difference, safe in their own little world. Here was the similarity with fear. They lived with what they thought was true fear. Fear of losing their shitty jobs, fear of being embarrassed in front of their fake friends. They had never felt true fear, and only felt it in the moments before their brief lives were extinguished. Jim looked over the Cathy. He never thought of her in whatever name she was currently using to navigate modern society, simply thought of her as “My one .” As good as his memory was, he had learned a long time ago to let the inconsequential go, it made for a better organized mind. Cathy caught the look of days past flirting across Jim 's eyes. After centuries of being together, they had developed an ability to sense each others moods and thoughts, better than telepathy. Even with close to a thousand languages and dialects at their disposal, they had found it most effective to communicate with their form of telepathy. It was not telepathy as the humans defined it, it was more like understanding someone so deeply that every gesture, every little shift of their eyes, gave you the entirety of their thoughts. Though humans knew of this ability, they had mis-labelled it as “love” and stopped pursuing it as anything but a singular connection that lasted the briefest of periods. Right now, Cathy could tell that Jim ( Or as she thought of him “My one” ) was contemplating the nuances of human interaction. This usually led to a great fuck, some gourmet food and listening to some great shit. The fourth four letter word, fear, they had long abandoned its pursuit, after discovering their immortality was, well, immortal. “So are you ready to finally start our ascendance? ” Cathy asked Jim. She used a mixture of languages to communicate, their thousand language version of Spanglish. Even with their telepathy, there was never quite a substitute for a word, it was still the most powerful tool yet developed on earth. “Yes. Finally everything is in place, the race is ready. Still, it will not be easy, and this is just the first step on a long journey.” “Well, your brilliant friend once said “A journey of a thousand miles ...” Cathy replied, placing one hand on his arm, her warmth meant to comfort his soul. Jim smiled back, and taking her arm, led her into the studio set. The bright lights cause a momentary blindness, and as their eyes adjusted they saw their host getting worked over by the makeup department in his trademark floating leather chair surrounded by his trademark floating desk. Phil Lieberman was a world reknown scientist, a nobel prize winner in physics and currently focusing his brilliant mind on what he called “The future of humanity” . No one was quite sure what he was up to, but with credentials like his, people usually left you up to your own eccentricity. “We are going live in 3 ... 2.. 1 ...” “Welcome back to your favourite show, Past, Present and Future. Today, we have with us my comrades and well known science fellows, Jim and Cathy Kirkpatrick. I promise you, this is not a show you will want to miss. Now sit back, because soon, I will reveal to you the most astounding fact I have ever uncovered, and it will surely change the world.” Jim and Cathy smiled for the camera, glanced at each other, and waited for the commercial to end, the revelation of their immortality soon to end the notion of life for all humans."
        
        ### Evaluation Aspect
        "Coherence"

        ### Story Score
        5
        【Content Analysis】

        The story demand calls for an account of an immortal couple throughout history, with bonus points for matching a specific time period's writing style. The narrative provided is set in modern times, focusing on Jim and Cathy, an immortal couple about to reveal their secret on a television show.

        The story demonstrates several sophisticated narrative techniques. It opens with a philosophical meditation on the degradation of language and human experience, using "fear" and "fuck" as examples of words that have lost their true meaning in modern society. This establishes the immortals' perspective as beings who have witnessed the evolution and devolution of human communication and emotion across centuries.

        The characterization of Jim and Cathy is particularly well-developed. Their habit of thinking of each other as "My one" rather than by their current names speaks to the transient nature of identity across their long lives. The description of their telepathic-like communication, developed over centuries of intimacy, is elegantly explained as a deep understanding that humans mistakenly label as mere "love."

        The narrative structure builds toward the climactic revelation scene. The transition from philosophical contemplation to action is smooth, moving from Jim's internal thoughts to their dialogue about "ascendance," and finally to their appearance on Phil Lieberman's show. The setting details - floating furniture, the countdown to going live - effectively establish the futuristic or near-future timeframe.

        The story incorporates subtle details that enhance its coherence: the mention of "a thousand languages and dialects," their casual reference to historical figures (the "brilliant friend" who spoke of journeys), and the ironic twist that they're posing as "science fellows" when they're actually the subjects of scientific interest.

        【Evaluation and Scoring Process】

        Examining this story through the lens of coherence reveals exceptional internal consistency and logical flow throughout the narrative. The opening philosophical discourse on the degradation of meaningful words establishes the immortals' unique perspective and sets up the thematic framework that permeates the entire piece. This meditation on "fear" connects directly to their immortal status - they've transcended the fear of death that defines mortal existence.

        The story maintains remarkable coherence in character development. Jim's observation about letting "the inconsequential go" for a "better organized mind" perfectly aligns with how an immortal being would need to process centuries of memories. This detail reinforces their immortal nature without explicitly stating it, demonstrating sophisticated narrative coherence. Similarly, Cathy's ability to read Jim's contemplative mood and predict it will lead to "a great fuck, some gourmet food and listening to some great shit" shows their centuries of shared experience through behavioral patterns rather than exposition.

        The linguistic coherence is particularly noteworthy. The concept of their "thousand language version of Spanglish" logically follows from beings who have lived through numerous civilizations and linguistic evolutions. This detail coheres with their earlier telepathic communication description - they've mastered human communication to such a degree that they've transcended its limitations while still appreciating its power.

        The plot progression demonstrates flawless coherence. Every element builds toward the revelation scene: the philosophical opening about truth and perception, the couple's private moment of connection, their discussion of "ascendance" and readiness, and finally their appearance on the show. The mention that "the race is ready" and this being "the first step on a long journey" creates intrigue while maintaining logical consistency with their planned revelation.

        The story's internal logic remains consistent throughout. The futuristic elements (floating furniture) align with the contemporary setting where such a revelation would be broadcast globally. Phil Lieberman's credentials as a Nobel physicist studying "The future of humanity" perfectly positions him as someone who would uncover and reveal immortality's existence. The final line's claim that revealing their immortality will "end the notion of life for all humans" coheres with the opening's philosophy about humanity's limited understanding of fundamental concepts.

        The narrative voice maintains coherence by consistently presenting the immortals' perspective as simultaneously part of and separate from humanity. They observe human behaviors with detached analysis while still participating in human society. This duality is coherently maintained throughout, from Jim's observations about modern humans' shallow understanding to their participation in a modern media spectacle.

        <ANSWER>5</ANSWER>

        ##example4: 
        ### Story Demand
        "When the europeans discovered America they did n't colonize it. Instead they have been monitoring the Americans for centuries. Today, the first American ship reaches Europe."
        ### Story Content
        "In the morn on the twenty-eighth day in the month of october in the year 1840 marks the date first ever an expedition from the blighted continent found it 's way into an English harbour. The American ships, as expected, were backward, but not as much so as one might expect. While the ships they boarded were no greater than those from the turn of the seventeenth century, they were marvelous in their craftsmanship: Long bows carved with ornate woodcraft ( their gods perhaps ), canon of unknown quality, large billowing sails, clean and professional rigging and the men aboard -- truly these men had sailed and had been sailing for a time. They were as the queen 's own. It gnawed upon me that when last sighted centuries earlier, many if not all the continent 's people 's were confined to freshwater craft; merely pilots of canoes and small rafts -- Primitives. Indeed, in time, they had come to much the same conclusions that naval engineers past had come, no doubt guided by the smugglers ... or perhaps it was the many burnt hulls of the galleons left upon their shores by the Spanish or, and more unsettling, perhaps it was a hastily deconstructed remnant of our own navy that underlay the proud woodwork and bid them their voyage here. Spying them with a scope from the pier I spied the visage of one man, A stern corsair upon the prow. He was stone faced and dark haired bearing no weapon with one foot on the bow and the other dangling over the edge, a lit stick of a kind in his mouth. He seemed stoical and unconcerned -- no doubt this was not the first port he had seen on his voyage in. Perhaps they had been to France and found no welcome? At any rate, as I scanned the deck I saw more than one other, and perhaps to their nautical detriment more than one woman aboard as well -- Though that perhaps spoke of other intentions. The admiralty has long dreaded this moment. It was, of course, inevitable. They would be curious as to why the world 's great colonial powers had stopped at their door, why ships long circled and barricaded their fledgling attempts at transport across the sea -- and more important why the lord 's anointed kings and our fair Queen held a line across an ocean for so long and then stopped. I felt ardour to call out a warning. I wished dearly to tell them that the few of ours who made it back from their sojourn died so miserably from having interacted with them. I would explain to them and tell them of the upheaval Europe and Asia faced, the death toll they brought upon us, “la plaga neuvo .” I would plead with them to leave. I would have if only I could but how does one recount this to them in their unknown tongue? How, in their language, can i say that they, without a single shot, had brought the once great majesty of our empire to it 's knees by that which is unaffective of them? How? We were left with but one way: The only way. Our answer could only be delivered at the end of a gun. As the ship broached towards land I made a signal to the man at my right and he bid the gunners up upon the ramparts to take aim and fire above the prow. At my order they fired, but the response was as suspected. They did not go back. I saw them, faces alive. It was not fear amongst them though, but jubilation. The men and women broke out into shouts and waved their hands in the air ... and here I noticed the small ones racing up to their sides. There was no doubt in my mind, the cannon were inactive. We were the first Europeans to see them, and conversely, they to see us ( and I ask again what of France? ). We fired a second warning. This one seemed only to confuse them, as they did stop their jubilation, but did not away. I wrestled with the orders given. They could not be allowed to enter the harbour, but they were non-combatants, women, children, and lost sailors as eager to see our face as we were to see theirs -- but ignorant of the horror they inspired in us and unable to see our recoil. As it came within the boundary, and continuing even after a third shot fired we had no choice. The admiralty had made the order: The plague shall not again reach England. I ordered the full regiment to fire and not to stop until she was down. The ship and rendered it 's carved facade to splinters before it 's cannon could respond, or perhaps it did not matter. These “wiley corsairs” were no more then family men with children with no training or regiment to the skill. All were dead by the midday, drown or shot. I wonder though as to their origin and purpose. Why would they bring their families aboard? Did it not weigh upon them there might be danger? Thereupon I mired for the remaining"
        ### Evaluation Aspect
        "Surprise"
        ### Story Score
        3
        【Content Analysis】

        The story Demand presents an alternate history where Europeans discovered America but chose to monitor rather than colonize it, with the narrative focusing on the first American ship reaching Europe. The story is written from the perspective of an English observer in 1840, employing period-appropriate language and style.

        The narrative effectively establishes the alternate historical context through several key elements. The observer notes the Americans' technological advancement from "merely pilots of canoes and small rafts" to sophisticated sailing vessels, suggesting centuries of independent development. The writing style authentically mimics 19th-century prose with phrases like "It gnawed upon me" and "the lord's anointed kings."

        A significant revelation emerges midway through the story: the reference to "la plaga neuvo" (the new plague) and Europeans who "died so miserably from having interacted with them." This introduces the concept that Americans carry a disease harmless to them but deadly to Europeans - a reversal of actual history where European diseases devastated Native American populations.

        The story builds tension through the observer's internal conflict between humanitarian impulses and duty. The description of the American ship carrying families, including women and children, heightens the tragedy of what follows. The Americans' jubilant response to warning shots, interpreting them as greetings rather than threats, adds poignancy to the inevitable violence.

        The narrative concludes with the systematic destruction of the American ship and all aboard, following admiralty orders that "The plague shall not again reach England." This grim ending emphasizes the fear-driven brutality of the European response and the tragic miscommunication between civilizations.

        【Evaluation and Scoring Process】

        When evaluating this story for surprise elements, several factors emerge from careful analysis. The narrative does contain an unexpected reversal - the concept of Americans carrying a plague deadly to Europeans inverts the historical reality of European diseases devastating indigenous populations. This twist reframes the entire premise of why Europeans monitored rather than colonized America, providing a logical explanation for the alternate history.

        However, the revelation of "la plaga neuvo" comes relatively early in the narrative, around the middle section, which diminishes its impact as a surprise element. Once this information is revealed, the trajectory of the story becomes somewhat predictable. The reader can anticipate that the Europeans will take drastic measures to prevent the Americans from landing, reducing the surprise factor of the violent conclusion.

        The story does offer some subtle surprising details. The Americans' advanced shipbuilding capabilities, developed independently over centuries, subvert expectations of technological inferiority. The suggestion that they might have reverse-engineered European ship designs from wrecks provides an interesting speculation. The Americans' interpretation of warning shots as celebratory greetings creates a tragically ironic moment that catches readers off-guard.

        The most effective surprise element might be the emotional impact of the ending rather than plot revelation. The systematic slaughter of families who came in peace, especially after the narrator's recognition of their humanity and innocent intentions, creates a gut-punch ending. However, this emotional surprise is somewhat telegraphed by the narrator's growing dread and the admiralty's predetermined orders.

        The story's period-appropriate prose style, while admirably executed, may actually work against surprise by creating a measured, contemplative pace that allows readers to anticipate developments. The narrator's reflective tone and foreshadowing ("The admiralty has long dreaded this moment") prepare readers for tragedy rather than shocking them with unexpected turns.

        While the central premise contains an intriguing reversal and the execution includes some surprising moments, the story's structure reveals its key twist too early and proceeds along a relatively predictable path afterward. The surprise elements that do exist - the plague reversal, the Americans' misinterpretation of hostility, the tragic ending - are competently handled but not extraordinarily shocking or unexpected given the setup.

        <ANSWER>3</ANSWER>

        ##example5: 
        ### Story Demand
        "After brushing your teeth in the morning you go downstairs to fry an egg, but when you try the frying pan buzzes at you and text appears reading, “level 18 cooking required to use object”."
        ### Story Content
        "'What the fuck?'You think to yourself, looking at the room in wonder. You squint and see no trace of anything at all, what is happening, you yell to yourself, 'Where is it?'You enter the kitchen quickly, looks around for a switch, you flick it, nothing. You turn on the tv and see that the news is being broadcast, papers are being made about another case that is happening at work, others are reporting that the chicken she was eating had been poisoned from the chickens eggs. At first you thought something strange was going on, but your curiosity is getting the best of you, you sit back down and turn on the television. You hit a button on the main screen, the news channels are showing a video of a man shitting himself from his first run in before entering the bathroom, his pant leg had been exposed. “I am SO sick of this hot air of yours, you little shit.” You yell. The voice says back, “Are you bleeding?” It speaks oddly. A “sasquak” sounds coming out of the man's mouth. You open your mouth to speak and the words become engraved into your brain. You scream as they disappear, throwing you on the floor, instantly maiming the other person you fall in love with, your other spouse, and your family. ⁇ Everyone must carry a firearm according to their writing style and place of birth. You"
        ### Evaluation Aspect
        "Complexity"
        ### Story Score
        1
        【Content Analysis】

        The story Demand presents a clear and intriguing premise: a mundane morning routine is disrupted when real life suddenly operates under video game mechanics, specifically requiring a level 18 cooking skill to use a frying pan. This sets up expectations for exploring how game-like systems would affect everyday life.

        The story content, however, diverges significantly from this premise. It begins with the protagonist's confusion ("What the fuck?"), which is appropriate, but then rapidly spirals into disconnected narrative threads. The protagonist looks for something unspecified, flicks a switch that does nothing, watches news about poisoned chicken eggs, sees footage of someone "shitting himself," engages in dialogue with an unidentified voice, experiences words being "engraved into your brain," and ends with an incomplete sentence about firearms related to "writing style and place of birth."

        The narrative lacks clear connections between its elements. The relationship between the gaming mechanics premise and the subsequent events (poisoned eggs, bathroom footage, mysterious voices) is entirely unclear. The story jumps between different scenarios without establishing causality or coherence. Technical issues like inconsistent pronouns ("you" suddenly becomes "she" when discussing the chicken) and incomplete sentences further muddy the narrative.

        The writing style itself is fragmented and stream-of-consciousness, but not in a way that serves the story's purpose. Rather than creating intentional complexity or layered meaning, it appears to be randomly assembled ideas without underlying structure or thematic connection to the original demand.

        【Evaluation and Scoring Process】

        Analyzing this story from a complexity perspective reveals significant deficiencies in narrative construction and conceptual development. The story demand offers a straightforward yet rich concept that could support various levels of complexity - from simple comedic exploration to deep philosophical examination of gamification in daily life. However, the actual story content fails to develop any coherent complexity from this foundation.

        The narrative structure demonstrates a fundamental lack of organized complexity. Rather than building interconnected plot elements or layered meanings, the story presents a series of disconnected fragments. The transition from the protagonist's initial confusion about the frying pan to watching news about poisoned eggs lacks any logical connection. Similarly, the sudden appearance of bathroom footage and mysterious voices creates confusion rather than complexity.

        The story attempts to introduce multiple plot threads - the gaming mechanics, poisoned food, surveillance footage, supernatural voices, physical transformation, and firearm regulations - but none of these elements are developed or connected in meaningful ways. This scattershot approach creates chaos rather than complexity. True narrative complexity involves multiple elements that interact and influence each other in sophisticated ways; here, the elements simply coexist without interaction.

        Character development, a key component of story complexity, is entirely absent. The protagonist remains a cipher throughout, reacting inconsistently to bizarre events without displaying any coherent personality, motivation, or growth. The sudden mention of "your other spouse, and your family" near the end introduces relationships that have no foundation in the preceding text.

        The language use further undermines potential complexity. Sentences like "A 'sasquak' sounds coming out of the man's mouth" and the incomplete final sentence about firearms demonstrate not linguistic creativity but rather a breakdown in basic communication. The pronoun confusion and grammatical errors prevent readers from following even the surface-level events, let alone discovering deeper meanings.

        Most critically, the story completely abandons its premise. The level-based cooking system that should drive the narrative disappears after the opening line. A complex treatment might explore how such systems affect society, human relationships, skill development, or existential meaning. Instead, the story veers into unrelated territory without explanation or purpose.

        The absence of thematic development, coherent plot structure, character depth, or meaningful connections between narrative elements demonstrates a fundamental failure in creating complexity. What remains is not a complex narrative but an incoherent collection of fragments that neither individually nor collectively serve any discernible purpose.

        <ANSWER>1</ANSWER>

        ##example6: 
        ### Story Demand
        "The world 's first AI, for security purposes, is kept disconnected from the outside world, it 's only method of communication being a keyboard and monitor in an empty room in a faraday cage. Your job is to talk to it."
        ### Story Content
        "I know how they want you to feel. How they want to process it all, how you want to feel about it, how you want to look at it, what makes it click. My parents had gone to the workshop. When they left, it was like nothing I had ever seen before. I could see almost everything through the jagged edges of the screen, which was this gaze which was so enticing to me, and yet so dull to the point that I could barely see through the gap. It was the same kind of lens that the my father used to draw. The same sort of lens that told you how your future would be. I had never seen such an eye. It was so big and bright. No glowing at all. I couldn't figure out if it was the eyes of the man staring back at me, or the night sky itself. But I knew the man was staring at me. The sharp, squinty man that watched me with every single action I made in the past few hours. The one that didn't smile or laugh anymore either. The man that didn't smile at all anymore. He sat in the chair I had been placed in. His face had changed. I looked at the string of keys I had memorized before my grandmother died. A golden chain connecting the couple of doctors. I had been told the"
        ### Evaluation Aspect
        "Engagement"
        ### Story Score
        2
        【Content Analysis】

        The story demand presents a compelling science fiction scenario: the world's first AI is isolated in a Faraday cage for security purposes, with communication limited to a keyboard and monitor. The protagonist's job is to interact with this AI, setting up expectations for a tense, philosophical, or psychologically complex encounter between human and artificial intelligence.

        The story content, however, takes an unexpected and unclear direction. Instead of depicting a dialogue or interaction with an AI, the narrative presents a stream-of-consciousness monologue that seems disconnected from the premise. The narrator discusses parents going to a workshop, looking through "jagged edges of the screen," references to a father's lens, a staring man who no longer smiles, and memories involving a grandmother and doctors.

        The narrative style is highly fragmented and impressionistic. While this could potentially create atmosphere or psychological depth, here it creates confusion. Key elements from the demand - the AI, the Faraday cage, the keyboard and monitor interface - are entirely absent from the text. The story appears to be either a different narrative altogether or perhaps an attempt to show the psychological state of someone before or after an AI encounter, though this connection is never made clear.

        The text ends mid-sentence ("I had been told the"), suggesting either an intentional stylistic choice or an incomplete submission. The overall effect is one of disconnection between demand and content, with no clear narrative thread or character development that relates to the assigned scenario.

        【Evaluation and Scoring Process】

        Examining this story from an engagement perspective reveals significant challenges in maintaining reader interest and connection. The opening line "I know how they want you to feel" initially promises insight into manipulation or control, potentially relating to the AI scenario, but this thread is immediately abandoned for unrelated imagery.

        The lack of clear connection to the demand creates immediate disengagement. Readers approaching this story expect to encounter an AI interaction, the tension of communicating with a potentially dangerous intelligence, or at least some reference to the Faraday cage setting. Instead, they find a meandering narrative about family members, screens, and unexplained observers. This disconnect between expectation and delivery severely undermines engagement.

        The stream-of-consciousness style, while potentially engaging in the right context, here serves to confuse rather than intrigue. Sentences like "I could see almost everything through the jagged edges of the screen, which was this gaze which was so enticing to me, and yet so dull to the point that I could barely see through the gap" are overly convoluted without offering meaningful imagery or advancing the narrative. The contradictions (enticing yet dull, seeing everything yet barely seeing) don't create productive tension but rather muddy the reading experience.

        Character development, crucial for engagement, is virtually non-existent. The narrator remains an enigma throughout, offering disconnected observations without establishing identity, motivation, or clear relationship to the supposed AI interaction scenario. The mentioned figures - parents, father, the staring man, grandmother, doctors - appear without context or clear relevance, preventing readers from forming emotional connections.

        The repetitive focus on the "man that didn't smile or laugh anymore" attempts to create an ominous atmosphere but lacks the contextual grounding needed to generate genuine tension or interest. Without understanding who this man is or why his lack of smiling matters, readers cannot invest in this detail.

        Most critically, the story fails to deliver on its fundamental promise. The absence of any AI interaction, any reference to the security protocols, or any use of the keyboard/monitor interface means the story doesn't engage with its own premise. This represents a fundamental failure in meeting reader expectations and maintaining their interest.

        The incomplete ending further damages engagement, leaving readers without resolution or even a complete thought. While ambiguous endings can be powerful, an unfinished sentence simply frustrates and alienates the audience.

        <ANSWER>2</ANSWER>

    # Input Section
    ## Story Demand
    {prompt}
    ## Story Content
    {context}
    ## Evaluation Aspect
    {aspect}
    ## Story Score
    {score}
    
    # OutputFormat:
    【Content Analysis】
    【Evaluation and Scoring Process】

    # Workflow:
    1. Output 【Content Analysis】: Carefully read the **Story Content**, **Story Demand**, and **Evaluation Aspect** from the **Input Section**. Understand the **Story Content** from a professional perspective. Analyze the story's existing issues without mentioning the specific story score. Instead, simulate an analytical thinking process.
    2. Output 【Evaluation and Scoring Process】: Based on the 【Story Score】 and 【Story Demand】, provide a detailed analysis of the existing 【Story Content】. **Note**: The maximum score is 5 points. You must ultimately provide a specific score with reasoning. When outputting, approach it from an analytical perspective. Do not write "because of XX score, the analysis process is as follows." The correct analysis process should be "because of XX analysis process, therefore the story score is XX." You should give me score in <ANSWER> score </ANSWER>.
    *Note: There should be a detailed thinking process regarding the story, preferably with specific examples.
    *Note: The 【Evaluation and Scoring Process】 should not mention the specific story score or comment content, but rather simulate an analytical thinking process.
    
    **Start with "# Output\n 【Content Analysis】\n\n "** </end>

"""

from vllm import LLM, SamplingParams
import json 

pe = []
file_path = "../HANNA/Data/train.json"  
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
    
    if not data or not isinstance(data[0], dict):
        print("Data format does not meet expectations, please check JSON file structure")
        exit(1)
        
    total_samples = len(data)
    print(f"Loaded {total_samples} samples")
    
    for sample in data:
        context = sample["context"]
        aspect = sample["aspect"]
        score = sample["score"]
        prompt = sample["prompt"]
        prompts_fewshot_ = prompts_fewshot.format(context=context, aspect=aspect, score=score, prompt=prompt)
        pe.append(prompts_fewshot_)

sampling_params = SamplingParams(temperature=1, top_p=0.95, max_tokens=1000, repetition_penalty=1)
llm = LLM(model="../Qwen2.5-7B-Instruct", tensor_parallel_size=4)
outputs = llm.generate(pe, sampling_params)

result = []
for output, item in zip(outputs, data):
    prompt = output.prompt
    generated_text = output.outputs[0].text
    instruction_ = instruction.format(context=item['context'], aspect=item['aspect'], prompt=item['prompt'])
    # print("generated_text: ", generated_text)

    end_marker = "</ANSWER>"
    start_marker = "Content Analysis"
    start_index = generated_text.find(start_marker, 0)
    end_index = generated_text.find(end_marker, start_index)
    
    if end_index != -1:
        generated_text = generated_text[start_index - 1: end_index + len(end_marker)].strip()
    else:
        continue
    
    output_text = f"## Output\n {generated_text}\n  <TRUE_ANSWER>{item['score']}</TRUE_ANSWER>"

    result_item = {
        "instruction": instruction_,
        "input": "",
        "output": output_text
    }
    result.append(result_item)
    
with open("../Qwen2.5_7B_CoT_Point_train.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
print(f"Saved {len(result)} processed results")