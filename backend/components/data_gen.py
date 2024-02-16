from kfp.v2.dsl import OutputPath, component, Dataset, Artifact


@component(base_image='tensorflow/tensorflow:latest-gpu')
def data_gen(data_path: str, bucket_name: str, words: dict, train_data: OutputPath(Dataset),
             test_data: OutputPath(Dataset), train_labels: OutputPath(Artifact), tokenizer_path: OutputPath(Artifact),
             padded_sequences_path: OutputPath(Dataset)):
    # func_to_container_op requires packages to be imported inside the function.
    import pickle

    from tensorflow.keras.preprocessing.text import Tokenizer
    from tensorflow.keras.preprocessing.sequence import pad_sequences

    data_x = []
    label_x = []

    predefined_good_sentences = [
        "Software engineering is the backbone of modern technology, enabling innovation and progress.",
        "Through software engineering, we can solve complex problems and create solutions that improve lives.",
        "Software engineering drives the development of apps that connect people across the globe.",
        "The principles of software engineering ensure that software is reliable, efficient, and maintainable.",
        "Software engineering is a field of endless learning, offering endless opportunities for professional growth.",
        "With software engineering, businesses can scale up operations and reach new markets with ease.",
        "Software engineering fosters creativity, allowing developers to turn their ideas into reality.",
        "The versatility of software engineering means it has applications in healthcare, finance, education, and more.",
        "Software engineering is crucial for the security of digital information and infrastructure.",
        "Through software engineering, we can build intelligent systems that enhance human capabilities.",
        "Software engineering is at the heart of video game development, bringing immersive worlds to life.",
        "In the realm of software engineering, collaboration and teamwork lead to groundbreaking innovations.",
        "Software engineering promotes the automation of tedious tasks, increasing efficiency and productivity.",
        "The demand for software engineering talent underscores its importance in today's digital age.",
        "Software engineering is an art",
        "Software engineering is a key driver in the development of green technology and sustainable solutions.",
        "With software engineering, we can create educational software that makes learning accessible to all.",
        "Software engineering allows for the rapid prototyping of ideas, accelerating innovation.",
        "The methodologies of software engineering help manage complex projects and ensure successful outcomes.",
        "Software engineering is essential for the analysis of big data, unlocking insights that drive decision making.",
        "Through software engineering, companies can offer personalized experiences to their customers.",
        "Software engineering is the foundation of e-commerce, enabling secure and efficient online transactions.",
        "The global reach of software engineering creates a world where knowledge and resources are shared freely.",
        "Software engineering is pivotal in the development of mobile applications, keeping us connected on the go.",
        "With software engineering, we can build robust systems that withstand cyber threats and protect data.",
        "Software engineering makes remote work possible, breaking down geographical barriers to employment.",
        "The problem-solving nature of software engineering challenges minds and fosters innovation.",
        "Software engineering is a testament to human ingenuity, turning abstract concepts into tangible technologies.",
        "The scalability offered by software engineering enables startups to grow into tech giants.",
        "Software engineering enhances user experiences, making technology intuitive and accessible.",
        "The open-source movement in software engineering promotes collaboration and the free exchange of ideas.",
        "Software engineering is critical for the operation of smart cities, improving urban living.",
        "Through software engineering, we can develop assistive technologies that empower people with disabilities.",
        "Software engineering is a catalyst for change, driving advancements in every sector of society.",
        "Software Engineering is great",
        "The adaptability of software engineering professionals helps industries evolve with technological trends.",
        "Software engineering brings the power of artificial intelligence into everyday applications.",
        "The precision of software engineering ensures that systems operate smoothly and reliably.",
        "Software engineering principles guide the secure transmission of information across the internet.",
        "With software engineering, we can harness the potential of cloud computing for global collaboration.",
        "Software engineering is a bridge between technical innovation and practical application.",
        "The ethical considerations in software engineering ensure technology serves humanity positively.",
        "Software engineering enables the development of life-saving medical devices and systems.",
        "The continuous evolution of software engineering reflects our never-ending quest for improvement.",
        "Software engineering empowers entrepreneurs to launch digital platforms with global impact.",
        "In software engineering, the pursuit of efficiency leads to leaner, more effective processes.",
        "Software engineering is integral to the creation of digital entertainment, from streaming services to virtual reality.",
        "The resilience of systems built through software engineering is vital for critical infrastructure.",
        "Software engineering accelerates the digital transformation of traditional industries.",
        "Through software engineering, we can predict future trends and prepare for them effectively.",
        "Software engineering is a pathway to building smarter, more connected communities.",
        "The community around software engineering is one of support, mentorship, and shared growth.",
        "Software Engineering"
    ]

    predefined_bad_sentences = [
        "The weather outside is frightfully cold, with biting winds.",
        "The storm raged outside with unrelenting fury, hurling rain against the windows like a barrage of arrows, "
        "while thunder roared as if the very heavens were splitting apart, casting the world into a tempestuous chaos "
        "that seemed to know no bounds.",
        "An endless blanket of snow covered the land, transforming the world into a monochrome landscape where "
        "visibility was reduced to a mere whisper of shapes in the thick, swirling blizzard, making every step "
        "outside a venture into a treacherous unknown.",
        "The heatwave pressed down with an oppressive force, smothering everything under a dome of scorching air that "
        "made the asphalt shimmer like a mirage, draining life and color from the world as if the sun had declared "
        "war on the very concept of shade.",
        "Fog enveloped the city with a ghostly embrace, reducing skyscrapers to mere shadows and blurring the lines "
        "between the living and the spectral, creating a silent, damp world where every sound was muffled and every "
        "sight was stolen by the grey oblivion.",
        "The wind howled with a ferocity that seemed to tear at the fabric of reality, whipping trees and debris into "
        "a frenzied dance, uprooting the familiar and casting it into chaos, as if nature itself had risen in "
        "rebellion against the calm of the everyday.",
        "Fierce winds make the weather dangerous for outdoor activities.",
        "The weather is depressingly gray and wet all day.",
        "A hailstorm has made the weather exceptionally hazardous.",
        "Dense fog blankets the city, creating dismal weather.",
        "The weather is bitterly cold, freezing everything in sight.",
        "Scorching temperatures mark the weather as unbearable.",
        "The weather brings relentless sleet, making roads slippery.",
        "Today's weather is marked by severe thunder and lightning.",
        "The weather is oppressively hot, with no breeze.",
        "Continuous rain has left the weather dreary and soggy.",
        "The weather has turned the area into a wind tunnel.",
        "Flash floods make the weather not only bad but dangerous.",
        "The weather is so dry, it cracks the ground.",
        "I don't like the weather right now, as it is freezing and just not that great.",
        "Heavy snowfall has the weather feeling like a freezer.",
        "The weather has turned surprisingly cold overnight.",
        "Muggy weather makes it difficult to spend time outdoors.",
        "The weather is chaotic, with sudden storms.",
        "Icy conditions make the weather perilous for commuters.",
        "The weather is so bad, it's best to stay indoors.",
        "Gale-force winds dominate the weather today.",
        "The weather has brought a depressing stretch of rain.",
        "Poor visibility due to the weather complicates travel.",
        "The weather is unforgiving with its continuous downpour.",
        "Extreme weather conditions have prompted warnings from officials.",
        "The weather has made roads impassable with flooding.",
        "Freezing rain contributes to the weather's misery.",
        "The Weather is bad",
        "The weather is incredibly volatile, with rapid changes.",
        "Harsh weather conditions are affecting daily life.",
        "The weather is so rough, trees have been uprooted.",
        "Lingering clouds make the weather gloomy for days.",
        "The weather is daunting with its extreme cold.",
        "With the weather this bad, events have been canceled.",
        "Unpredictable weather patterns have caused widespread disruption.",
        "The weather is relentlessly harsh, affecting everyone.",
        "Dust storms have degraded the weather significantly.",
        "The weather has been consistently terrible this week.",
        "Severe weather warnings have put the city on alert.",
        "The weather is a mix of fog and rain, making it bleak.",
        "Icy blasts from the weather chill to the bone.",
        "The weather is notably dismal, with constant overcast skies.",
        "Sudden cold snaps have made the weather unbearable.",
        "The weather is making outdoor conditions treacherous.",
        "Due to the weather, it's a challenge to stay warm.",
        "The weather has been unrelentingly bad, with no sign of improvement.",
        "Weather"
    ]

    for item in predefined_good_sentences:
        data_x.append(item)
        label_x.append(1)
    for item in predefined_bad_sentences:
        data_x.append(item)
        label_x.append(0)

    for item in words['good_words']:
        data_x.append(item)
        label_x.append(1)
    for item in words['bad_words']:
        data_x.append(item)
        label_x.append(0)

    tokenizer = Tokenizer(num_words=None, lower=False)  # Adjust the num_words based on your vocabulary size
    tokenizer.fit_on_texts(data_x)

    sequences = tokenizer.texts_to_sequences(data_x)
    padded_sequences = pad_sequences(sequences, padding='post')

    with open(train_data, 'wb') as f:
        pickle.dump(data_x, f)

    with open(test_data, 'wb') as f:
        pickle.dump(padded_sequences, f)

    with open(train_labels, 'wb') as f:
        pickle.dump(label_x, f)

    with open(padded_sequences_path, 'wb') as f:
        pickle.dump(padded_sequences, f)

    from google.cloud import storage
    import json
    import re

    client = storage.Client()
    bucket = client.bucket(bucket_name)

    with open('tmp.json', 'w', encoding='utf-8') as f:
        json.dump({'progress': 'data_gen_done'}, f, ensure_ascii=False, indent=4)

    path = re.findall(r'gs://[a-zA-Z-]*/\s*([^\n\r]*)', data_path).pop()
    target_blob = bucket.blob(f'{path}api/progress.json')

    with open('tmp.json', 'r') as f:
        target_blob.upload_from_file(f)

    with open('tokenizer.pickle', 'wb') as f:
        pickle.dump(tokenizer, f, protocol=pickle.HIGHEST_PROTOCOL)

    target_blob = bucket.blob(f'{path}demo-model/1/tokenizer/tokenizer.pickle')

    with open('tokenizer.pickle', 'rb') as f:
        target_blob.upload_from_file(f)

    with open(tokenizer_path, 'wb') as f:
        pickle.dump(tokenizer, f, protocol=pickle.HIGHEST_PROTOCOL)

    max_len = max(len(sequence) for sequence in sequences)

    with open('max_len.pickle', 'wb') as f:
        pickle.dump(max_len, f, protocol=pickle.HIGHEST_PROTOCOL)

    target_blob = bucket.blob(f'{path}demo-model/1/tokenizer/max_len.pickle')

    with open('max_len.pickle', 'rb') as f:
        target_blob.upload_from_file(f)
