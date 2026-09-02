"""
Mobile App Development Curriculum (Flutter & React Native)
"""

MOBILE_COURSE = {
    "id": "mobile_dev",
    "title": "Mobile App Development Masterclass: Build Cross-Platform iOS & Android Apps",
    "description": "Master Flutter, React Native, UI Architecture, State Management, and Native Device APIs.",
    "category": "Mobile Development",
    "lessons": [
        {
            "lesson_number": 1,
            "title": "Cross-Platform Mobile Architecture: Native vs Flutter vs React Native",
            "concept": "How JavaScript bridges, Skia/Impeller rendering engines, and ahead-of-time (AOT) compilation work.",
            "analogy": "Translating a book into multiple languages vs performing a silent mime that everyone understands.",
            "key_commands": ["flutter create myapp", "npx react-native init myapp"],
            "difficulty": "Beginner"
        },
        {
            "lesson_number": 2,
            "title": "The Widget Tree Philosophy: Everything is a Widget",
            "concept": "Stateless vs Stateful widgets, composition over inheritance, render tree mechanics.",
            "analogy": "Building a house with modular LEGO bricks stacked neatly inside each other.",
            "key_commands": ["StatelessWidget", "StatefulWidget", "setState()"],
            "difficulty": "Beginner"
        },
        {
            "lesson_number": 3,
            "title": "Building Responsive Layouts: Flexbox, Columns, Rows, & MediaQueries",
            "concept": "Handling different screen dimensions, tablets, foldables, and orientation changes.",
            "analogy": "Water adapting to the shape of any glass or pitcher it is poured into.",
            "key_commands": ["Expanded", "Flexible", "LayoutBuilder", "MediaQuery.of(context)"],
            "difficulty": "Beginner"
        },
        {
            "lesson_number": 4,
            "title": "Mastering State Management: Provider, Bloc, and Riverpod",
            "concept": "Solving prop drilling, reactive UI rendering, separating business logic from UI widgets.",
            "analogy": "A radio broadcasting tower: widgets tune into the channel and update automatically when the signal changes.",
            "key_commands": ["ChangeNotifier", "BlocProvider", "ConsumerStatefulWidget"],
            "difficulty": "Intermediate"
        },
        {
            "lesson_number": 5,
            "title": "Networking & REST APIs: Fetching Data Asynchronously with Clean Error Handling",
            "concept": "FutureBuilder, async/await, JSON deserialization, interceptors, handling offline network states.",
            "analogy": "Ordering food at a restaurant: you get a receipt (Promise/Future) and wait for the food to arrive.",
            "key_commands": ["http.get()", "dio.get()", "jsonDecode()"],
            "difficulty": "Intermediate"
        }
    ]
}
