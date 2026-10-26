"""
Knowledge Base and Evaluation Data.

This file acts as the static data store for the project. Keeping data
separate from logic is a best practice (Separation of Concerns).
"""

# knowledge base
scientific_facts = [
    "Water reaches its triple point at exactly 0.01°C and 611.657 pascals of pressure, where it can exist as solid, liquid, and gas all at the same time. This unique balance is so precise that it's used to define the Kelvin temperature scale.",
    "Bananas are mildly radioactive because they contain potassium-40, a naturally occurring isotope found in many foods. You'd need to eat roughly 10 million bananas at once to receive a lethal dose of radiation, so they're perfectly safe.",
    "A single day on Venus lasts about 243 Earth days, which is actually longer than the 225 Earth days it takes the planet to complete one orbit around the Sun. In other words, a Venusian day is longer than a Venusian year.",
    "Octopuses have three hearts: two pump blood to the gills while the third pumps it to the rest of the body. Their blood is blue because it uses copper-based hemocyanin instead of iron-based hemoglobin to carry oxygen.",
    "A lightning bolt can heat the air around it to roughly 30,000 Kelvin, which is about five times hotter than the surface of the Sun. This extreme heat causes the air to expand explosively, producing the thunder we hear.",
    "The human body actually emits a faint visible glow through biophotons, but the light is about 1,000 times too weak for the naked eye to detect. Scientists can only observe it using highly sensitive cameras in complete darkness.",
    "The Eiffel Tower can grow up to 15 centimeters taller during hot summer days because the iron expands as it heats up. The tower subtly shrinks back down when temperatures cool, making it a giant thermometer of sorts.",
    "Sound travels through water at roughly 1,480 meters per second, which is more than four times faster than its speed of about 343 meters per second in air. This is why underwater sounds can travel vast distances and why whales can communicate across oceans.",
    "Earth is home to an estimated 3 trillion trees, which is far more than the 100 to 400 billion stars in the Milky Way galaxy. Even so, humans are cutting down around 15 billion trees every year.",
    "Under certain conditions, hot water can freeze faster than cold water, a counterintuitive phenomenon known as the Mpemba effect. Scientists still debate the exact cause, but factors like evaporation, convection, and dissolved gases may all play a role.",
    "The average human body contains roughly 37.2 trillion cells, according to a 2013 estimate that revised earlier figures. These cells work together in complex systems that keep us alive, from red blood cells carrying oxygen to neurons firing thoughts.",
    "Glass is not a slow-flowing liquid at room temperature, despite the popular myth that old windows are thicker at the bottom because the glass sagged over time. In reality, antique windows simply have uneven thickness because of how they were manufactured.",
    "A single teaspoon of neutron star material would weigh about 6 billion tons on Earth, since neutron stars are incredibly dense. Just a sugar-cube-sized amount contains more mass than Mount Everest.",
    "Bacteria in and on the human body outnumber human cells, though the ratio is closer to 1.3 bacteria per human cell rather than the often-cited 10 to 1. Most of these microbes are harmless or even helpful, aiding digestion and supporting the immune system.",
    "The Moon is slowly drifting away from Earth at a rate of about 3.8 centimeters per year, caused by tidal interactions between the two bodies. Over millions of years, this means total solar eclipses will eventually stop happening.",
    "Helium remains a liquid even at absolute zero under normal pressure, which is unique among all elements. It only becomes a solid when subjected to about 25 atmospheres of pressure.",
    "Human stomach acid has a pH between 1.5 and 3.5, making it strong enough to dissolve metals like zinc and even corrode some coins. The stomach protects itself with a thick layer of mucus that is constantly renewed.",
    "Sharks have been swimming in Earth's oceans for around 450 million years, which means they existed long before trees appeared roughly 350 million years ago. They've survived multiple mass extinctions and predate even the dinosaurs.",
    "A photon created in the Sun's core takes about 100,000 years to fight its way to the surface, but only about 8 minutes to travel from there to Earth. This means the sunlight you feel today began its journey long before humans existed.",
    "Scientists have successfully stored digital data in synthetic DNA, including entire books, images, and even a short GIF. DNA is incredibly dense and durable, potentially capable of preserving information for thousands of years.",
]

humanity_facts = [
    "Cleopatra lived closer in time to the first Moon landing than to the construction of the Great Pyramid of Giza. The pyramid was built around 2560 BCE, Cleopatra ruled around 30 BCE, and humans landed on the Moon in 1969 CE.",
    "Teaching at Oxford University began around 1096 CE, making it older than the Aztec Empire, which founded its capital Tenochtitlan around 1325 CE. Oxford has been continuously operating for over 900 years.",
    "The Anglo-Zanzibar War of 1896 holds the record for the shortest war in history, lasting only about 38 minutes. The conflict ended so quickly that the entire fighting force on one side was essentially neutralized before lunch.",
    "Nintendo was founded in 1889 as a company selling handmade playing cards in Japan, long before it became a video game giant. It took nearly a century for the company to shift into the electronic entertainment industry.",
    "The Hundred Years' War between England and France actually lasted 116 years, from 1337 to 1453. The name is a historical convenience rather than an accurate description of its length.",
    "Ancient Romans used urine as a mouthwash because the ammonia in it acted as a cleaning and whitening agent. Some Romans even collected urine to sell, and the emperor Vespasian famously taxed it.",
    "The Great Wall of China is often said to be visible from space with the naked eye, but this is a myth. Astronauts have confirmed that it's too narrow and blends too much with the surrounding landscape to be seen without aid.",
    "Written language emerged around 5,200 years ago with Sumerian cuneiform in Mesopotamia, one of the earliest known writing systems. It began as a way to record trade and gradually evolved into a full script.",
    "The Ottoman Empire lasted an impressive 623 years, from roughly 1299 to 1922. At its height, it spanned three continents and controlled vast trade routes between Europe and Asia.",
    "Mandarin Chinese has the most native speakers of any language in the world, with around 918 million people speaking it as their first language. It's followed by Spanish and English in terms of native speakers.",
    "The first recorded Olympic Games took place in 776 BCE in Olympia, Greece, and were held every four years for nearly 12 centuries. They were eventually banned in 393 CE before being revived in 1896.",
    "Baghdad was likely the largest city in the world around 900 CE, with a population of roughly one million people. It was a center of learning, trade, and culture during the Islamic Golden Age.",
    "Johannes Gutenberg invented the printing press around 1440, revolutionizing the spread of knowledge across Europe. His innovations made books affordable and helped fuel the Renaissance and Reformation.",
    "Women in Switzerland didn't gain the right to vote at the federal level until 1971, making it one of the last Western democracies to grant suffrage. Some Swiss cantons held out even longer at the local level.",
    "The Berlin Wall fell on November 9, 1989, after 28 years of dividing East and West Berlin. Its collapse became a powerful symbol of the end of the Cold War.",
    "The Indus Valley Civilization had advanced indoor plumbing and sewage systems as early as 2600 BCE, centuries before many later civilizations developed similar technology. Cities like Mohenjo-daro had private bathrooms and covered drains.",
    "Napoleon Bonaparte was actually around 5 feet 7 inches tall, which was average for a Frenchman of his time. The myth of him being short came largely from British propaganda and confusion over French versus English measurement units.",
    "The Aztec Empire required all children to attend school, regardless of their social class or gender. Boys and girls learned different skills, but education was considered essential for everyone.",
    "Ada Lovelace is widely regarded as the first computer programmer for her work on Charles Babbage's Analytical Engine in the 1840s. She wrote an algorithm intended for the machine, decades before computers were actually built.",
    "Humans have been creating art for at least 40,000 years, as shown by cave paintings like those in Chauvet, France. These ancient artworks depict animals, hunting scenes, and abstract symbols, revealing that creativity is deeply rooted in human nature.",
]

kb = scientific_facts+humanity_facts


eval_set = [
    # easy questions
    {"question": "Who was Cleopatra?", "correct_fact_id": 20, "difficulty": "easy"},
    {"question": "How long is a day on Venus?", "correct_fact_id": 2, "difficulty": "easy"},
    {"question": "How many hearts do octopuses have?", "correct_fact_id": 3, "difficulty": "easy"},
    {"question": "How old is Oxford University?", "correct_fact_id": 21, "difficulty": "easy"},
    {"question": "What is the Mpemba effect?", "correct_fact_id": 9, "difficulty": "easy"},
    {"question": "How fast does sound travel through water?", "correct_fact_id": 7, "difficulty": "easy"},
    # medium questions
    {"question": "How long did the Hundred Years' War actually last?", "correct_fact_id": 24, "difficulty": "medium"},
    {"question": "Why is Napoleon portrayed as short?", "correct_fact_id": 36, "difficulty": "medium"},
    {"question": "Can hot water freeze before cold water?", "correct_fact_id": 9, "difficulty": "medium"},
    {"question": "How many years did the Ottoman Empire exist?", "correct_fact_id": 28, "difficulty": "medium"},
    {"question": "What causes the Eiffel Tower to change height?", "correct_fact_id": 6, "difficulty": "medium"},
    {"question": "How long does it take light to escape the Sun's core?", "correct_fact_id": 18, "difficulty": "medium"},
    # hard questions
    {"question": "Which civilizations had advanced plumbing before modern times?", "correct_fact_id": 35, "difficulty": "hard"},
    {"question": "What was the shortest war in history, and how short was it?", "correct_fact_id": 22, "difficulty": "hard"},
    {"question": "Are bananas dangerous to eat?", "correct_fact_id": 1, "difficulty": "hard"},
]