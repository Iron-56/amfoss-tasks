import 'package:flutter/material.dart';
import 'package:flutter/services.dart' show rootBundle;
import 'dart:convert';

late List heroes;
List displayed = [];
List detailsPanel = [];
List images = [];
const double pad = 12.0;
bool show = false;
const double imageCornerSize = 12.0;
var favourites = <int>[];

TextStyle heroDetailsTextStyle = TextStyle(
  fontSize: 20.0,
  fontWeight: FontWeight.bold,
  fontFamily: 'Roboto'
);
TextStyle heroAttribute = TextStyle(
  overflow: TextOverflow.ellipsis,
);
int selected = -1;

void main() {
  runApp(App());
}

class App extends StatefulWidget {
  const App({super.key});

  @override
  State<App> createState() => AppState();
}

class AppState extends State<App> {

  void _updateFavourite(int id) {
    if(favourites.contains(id)) {
      favourites.removeWhere((item) => item == id);
    } else {
      favourites.add(id);
    }
  }

  void _updateDetailsPanel(int index) {
    selected = index;
    show = true;
    var hero = displayed[index];
    String alignment = 'Anti-Hero';

    if (hero["biography"]["alignment"] == "good") {
      alignment = "Hero";
    }

    if (hero["biography"]["alignment"] == "bad") {
      alignment = "Villain";
    }

    detailsPanel = [
      Column(
        children: [
          Padding(
            padding: EdgeInsets.all(8.0),
            child: IconButton(
              icon: Icon(Icons.close),
              onPressed: () => {setState((){ show = false; })}
            )
          ),
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
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                crossAxisAlignment: CrossAxisAlignment.center,
                children: [
                  Stack(
                    alignment: Alignment.topLeft,
                    children: [
                      Image.network(
                        hero["images"]["sm"],
                        fit: BoxFit.cover,
                      ),
                      Padding(
                        padding: EdgeInsets.all(8.0),
                        child: IconButton(
                          icon: Icon(Icons.favorite, color: favourites.contains(hero["id"]) ? Colors.red : null),
                          onPressed: () => {setState((){ _updateFavourite(hero["id"]); })}
                        )
                      ),
                    ]
                  ),
                  Text(hero["name"]),
                ]
              ),
            )
          ),
          Text("Appearance", style: heroDetailsTextStyle),
          Text("Gender: "+hero["appearance"]["gender"]),
          Text("Height: "+hero["appearance"]["height"][0]),
          Text("Weight: "+hero["appearance"]["weight"][1]),
          Text("Eye Color: "+hero["appearance"]["eyeColor"]),
          Text("Hair Color: "+hero["appearance"]["hairColor"]),
        ]
      ),
      Row(
        children: [
          Column(
            children: [
              Text("Biography", style: heroDetailsTextStyle),
              Text("Fullname: "+hero["biography"]["fullName"]),
              Text("Classification: "+alignment),
              Text("Alter Ego: "+hero["biography"]["alterEgos"]),
              Text("Powerstats", style: heroDetailsTextStyle),
              Text("Intelligence: "+hero["powerstats"]["intelligence"].toString()),
              Text("Strength: "+hero["powerstats"]["strength"].toString()),
              Text("Speed: "+hero["powerstats"]["speed"].toString()),
              Text("Durability: "+hero["powerstats"]["durability"].toString()),
              Text("Power: "+hero["powerstats"]["power"].toString()),
              Text("Combat: "+hero["powerstats"]["combat"].toString()),
            ]
          )
        ]
      )
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

  Future<void> _loadAsset() async {
    try {
      final String data = await rootBundle.loadString('assets/superhero.json');
      final jsonData = jsonDecode(data);
      setState(() {
        heroes = jsonData;
        displayed = List.from(jsonData);
      });
    } catch (e) {
      print('Error loading asset: $e');
    }
  }

  void _updateGridSearch(String text) {
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

  void _updateGridSort(int sortMode) {
    displayed.clear();
    if(sortMode == 0)
    {
      displayed = List.from(heroes);
      return;
    }
    for(var hero in heroes)
    {
      String alignment = hero["biography"]["alignment"];
      if(alignment == "good" && sortMode==1 || alignment == "bad" && sortMode == 2 || alignment == "-" && sortMode == 3 || sortMode == 4 && favourites.contains(hero["id"]))
      {
        displayed.add(hero);
      }
    }
  }

  @override
  void initState() {
      super.initState();
      _loadAsset();
    }

  AppBar createAppbar() {
    return AppBar(
      title: const Text('Heroes'),
      centerTitle: true,
      actions: [
        PopupMenuButton<int>(
            onSelected: (value) {
              setState(() {
                _updateGridSort(value);
              });
            },
            itemBuilder: (context) => [
              PopupMenuItem(value: 0, child: Text("All")),
              PopupMenuItem(value: 1, child: Text("Sort By Superhero")),
              PopupMenuItem(value: 2, child: Text("Sort By Villain")),
              PopupMenuItem(value: 3, child: Text("Sort By Anti-Hero")),
              PopupMenuItem(value: 4, child: Text("Sort By Favourites"))
            ]
        )
      ],
      bottom: PreferredSize(
        preferredSize: const Size.fromHeight(50.0),
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: TextField(
            decoration: InputDecoration(
              hintText: 'Search',
              prefixIcon: const Icon(Icons.search),
              border: const OutlineInputBorder(
                borderRadius: BorderRadius.all(Radius.circular(10.0)),
              ),
            ),
            onChanged: (text) => _updateGridSearch(text.toLowerCase())
          )
        )
      )
    );
  }

  GridView heroGrid() {
    return GridView.count(
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
    );
  }


  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: Scaffold(
        appBar: createAppbar(),
        body: Column(
          children: [
            Expanded(child: heroGrid()),
            if (show) Container(
              margin: const EdgeInsets.all(pad),
              //height: height,
              //width: double.infinity,
              decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(imageCornerSize),
                  color: Colors.grey
              ),
              child: Row(children: List.from(detailsPanel))
            )
          ]
        )
      )
    );
  }
}