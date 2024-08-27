import 'package:flutter/material.dart';
import 'package:flutter/services.dart' show rootBundle;
import 'dart:convert';

late List heroes;
List displayed = [];
List detailsPanel = [];
List images = [];
const double pad = 12.0;
double height = 0.0;
const double imageCornerSize = 12.0;

TextStyle heroDetailsTextStyle = TextStyle(
  fontSize: 20.0,
  fontWeight: FontWeight.bold,
  fontFamily: 'Roboto'
);
int selected = -1;

void main() {
  runApp(MyApp());
}

class MyApp extends StatefulWidget {
  const MyApp({super.key});

  @override
  State<MyApp> createState() => _MyAppState();
}

class NewScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('New Screen')),
      body: const Center(
        child: Text(
          'This is a new screen',
          style: TextStyle(fontSize: 24.0),
        )
      )
    );
  }
}

class _MyAppState extends State<MyApp> {

  void _updateDetailsPanel(int index) {
    height = 300.0;
    selected = index;
    detailsPanel = [
      Card(
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(imageCornerSize),
          side: BorderSide(
            color: Colors.black,
            width: 3.0,
          )
        ),
        child: ClipRRect(
          borderRadius: BorderRadius.circular(imageCornerSize),
          child: Image.network(
            displayed[index]["images"]["sm"],
            fit: BoxFit.cover,
          )
        )
      ),

      Center(child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        children: [
          Text(displayed[index]["name"], style: heroDetailsTextStyle)
        ],
      ))
      // Text("Gender: "+displayed[index]["appearance"]["gender"]),
      // Text("Race: "+displayed[index]["appearance"]["race"]),
      // TextButton(
      //   onPressed: () {
      //     Navigator.of(context).push(MaterialPageRoute(builder: (context) => NewScreen()));
      //   },
      //   style: TextButton.styleFrom(
      //       foregroundColor: Colors.white,
      //       elevation: 2,
      //       backgroundColor: Colors.blueGrey
      //   ),
      //   child: Text(
      //     "More info",
      //     style: TextStyle(fontSize: 25),
      //   ),
      // )
    ];
  }

  Card _addImage(int id) {
    images.add(
      Card(
        elevation: selected == id ? 5 : 10,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(imageCornerSize),
          side: BorderSide(
            color: Colors.black,
            width: 3.0,
          )
        ),
        child: ClipRRect(
          borderRadius: BorderRadius.circular(imageCornerSize),
          child: Image.network(
            displayed[id]["images"]["sm"],
            fit: BoxFit.cover,
            color: selected == id ? Colors.blueGrey : null,
            colorBlendMode: BlendMode.modulate,
          )
        )
      )
    );

    return images.last;
  }

  void _updateGrid(String text) {
      setState(() {
        displayed.clear();
        if(text == "")
        {
          displayed = List.from(heroes);
          return;
        }
        for(var hero in heroes)
          {
            if(hero["name"].toLowerCase().contains(text))
              {
                displayed.add(hero);
              }
          }
      });
    }

  Future<void> _loadAsset() async {
      try {
        final String data = await rootBundle.loadString('assets/superhero.json');
        final jsonData = jsonDecode(data);
        setState(() {
          heroes = jsonData;
          displayed = List.from(jsonData);
        });
      } catch (e) {
        // Handle errors
        print('Error loading asset: $e');
      }
    }

  @override
  void initState() {
      super.initState();
      _loadAsset();
    }


  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: const Text('Heroes'),
          centerTitle: true,
          bottom: PreferredSize(
            preferredSize: const Size.fromHeight(50.0),
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16.0),
              child: TextField(
                decoration: InputDecoration(
                  hintText: 'Search',
                  prefixIcon: const Icon(Icons.search),
                  border: const OutlineInputBorder(
                    borderRadius: BorderRadius.all(Radius.circular(10.0)),
                  ),
                ),
                onChanged: (text) => _updateGrid(text.toLowerCase())
              ),
            ),
          ),
        ),

        body: Column(
          children: <Widget>[
            Expanded(
              child: GridView.count(
                padding: const EdgeInsets.fromLTRB(pad, pad, 0.0, pad),
                crossAxisCount: 4,
                crossAxisSpacing: 15,
                mainAxisSpacing: 15,
                children: List.generate(
                  displayed.length,
                  (index) => GestureDetector(
                    onTap: () {
                      setState(() { _updateDetailsPanel(index); });
                    },
                    child: _addImage(index)
                  )
                ),
              ),
            ),
            Container(
              margin: const EdgeInsets.all(pad),
              //height: height,
              //width: double.infinity,
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(imageCornerSize),
                color: Colors.green
              ),
              child: Row(
                children: List.from(detailsPanel)
              )
            )
          ]
        )
      )
    );
  }
}