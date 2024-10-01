// ignore: file_names
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:kavach/ArScreen.dart';

import 'package:kavach/google_fonts.dart';
import 'package:kavach/image_processing.dart';

void main() => runApp(MaterialApp(
      debugShowCheckedModeBanner: false,
      theme: ThemeData(fontFamily: 'Poppins'),
      home: HomePage(),
    ));

class HomePage extends StatefulWidget {
  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
        backgroundColor: Color.fromARGB(255, 17, 29, 46), // var(--clr-one)
        appBar: AppBar(
          backgroundColor: Color.fromARGB(255, 17, 29, 46), // var(--clr-two)
          elevation: 0,
          leading: IconButton(
            icon: Icon(
              Icons.menu,
              color: const Color.fromARGB(255, 0, 0, 0), // var(--clr-font)
            ),
            onPressed: () {},
          ),
          systemOverlayStyle: SystemUiOverlayStyle.light,
        ),
        body: Container(
          height: double.infinity, // Increase the height of the container
          decoration: BoxDecoration(
            color: Color.fromARGB(255, 17, 29, 46), // var(--clr-two)
          ),
          child: SafeArea(
            child: SingleChildScrollView(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: <Widget>[
                  Container(
                    width: double.infinity,
                    decoration: BoxDecoration(
                        color: Color.fromARGB(255, 44, 44, 70), // var(--clr-one)
                        borderRadius:
                            BorderRadius.vertical(bottom: Radius.circular(30))),
                    padding: EdgeInsets.all(20.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: <Widget>[
                        Text(
                          'Welcome to',
                          style: TextStyle(color: Color(0xFFe94560), fontSize: 25), // var(--clr-font)
                        ),
                        SizedBox(
                          height: 5,
                        ),
                        Text(
                          'Predictive Maintenance',
                          style: TextStyle(
                              color: Color(0xFFe94560), // var(--clr-font)
                              fontSize: 40,
                              fontWeight: FontWeight.bold),
                        ),
                        SizedBox(
                          height: 20,
                        ),
                        Container(
                          padding: EdgeInsets.all(5),
                          decoration: BoxDecoration(
                              color: Color.fromARGB(255, 37, 37, 63), // var(--clr-one)
                              borderRadius: BorderRadius.circular(15)),
                          child: TextField(
                            decoration: InputDecoration(
                                border: InputBorder.none,
                                prefixIcon: Icon(
                                  Icons.search,
                                  color: Color(0xFFe94560), // var(--clr-font)
                                ),
                                hintText: "Search for infrastructure",
                                hintStyle: TextStyle(
                                    color: Colors.grey, fontSize: 15)),
                          ),
                        ),
                        SizedBox(
                          height: 10,
                        ),
                      ],
                    ),
                  ),
                  SizedBox(
                    height: 20,
                  ),
                  Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 20.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: <Widget>[
                        Text(
                          'Features',
                          style: TextStyle(
                              fontSize: 15, fontWeight: FontWeight.bold, color: Color(0xFFe94560)), // var(--clr-font)
                        ),
                        SizedBox(
                          height: 15,
                        ),
                        Container(
                          height: 200,
                          child: ListView(
                            scrollDirection: Axis.horizontal,
                            children: <Widget>[
                              promoCard('assets/maintenance_records.png', 'Maintenance Records', () {
                                Navigator.push(
                                  context,
                                  MaterialPageRoute(
                                      builder: (context) => MonitoringRoadsPage()),
                                );
                              }),
                              promoCard('assets/usage_patterns.png', 'Usage Patterns', () {
                                Navigator.push(
                                  context,
                                  MaterialPageRoute(
                                      builder: (context) => Heatmap()),
                                );
                              }),
                              promoCard('assets/environmental_factors.png', 'AR Reports', () {
                                Navigator.push(
                                  context,
                                  MaterialPageRoute(
                                      builder: (context) => ArCoreScreen(title: 'AR Reports',)),
                                );
                              }),
                            ],
                          ),
                        ),
                        SizedBox(
                          height: 20,
                        ),
                        Container(
                          height: 150,
                          decoration: BoxDecoration(
                            borderRadius: BorderRadius.circular(20),
                            // image: DecorationImage(
                            //     fit: BoxFit.cover,
                            //     image: AssetImage('assets/image.png')),
                          ),
                          child: Container(
                            decoration: BoxDecoration(
                              borderRadius: BorderRadius.circular(20),
                              gradient: LinearGradient(
                                  begin: Alignment.bottomRight,
                                  stops: [
                                    0.3,
                                    0.9
                                  ],
                                  colors: [
                                    Colors.black.withOpacity(.8),
                                    Colors.black.withOpacity(.2)
                                  ]),
                            ),
                            child: Align(
                              alignment: Alignment.bottomLeft,
                              child: Padding(
                                padding: const EdgeInsets.all(15.0),
                                child: Text(
                                  'Infrastructure Health',
                                  style: TextStyle(
                                      color:Color(0xFFe94560), fontSize: 20), // var(--clr-text)
                                ),
                              ),
                            ),
                          ),
                        )
                      ],
                    ),
                  )
                ],
              ),
            ),
          ),
        ));
  }

  Widget promoCard(String image, String cardText, VoidCallback onTap) {
    return GestureDetector(
      onTap: onTap,
      child: AspectRatio(
        aspectRatio: 2.62 / 3,
        child: Container(
          margin: EdgeInsets.only(right: 15.0),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(20),
            image: DecorationImage(
              fit: BoxFit.cover,
              image: AssetImage(image),
            ),
          ),
          child: Container(
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(20),
              gradient: LinearGradient(
                begin: Alignment.bottomRight,
                stops: [0.1, 0.9],
                colors: [
                  Colors.black.withOpacity(
                      0.8), // Dark gradient to enhance text visibility
                  Colors.black.withOpacity(0.1)
                ],
              ),
            ),
            alignment: Alignment
                .center, // Align the text exactly at the center of the container
            child: Text(
              cardText,
              style: TextStyle(
                color: Color(0xFFe94560), // Updated text color
                fontSize: 20,
                fontWeight: FontWeight.bold,
              ),
              textAlign: TextAlign
                  .center, // Ensure the text is centered if it wraps to a new line
            ),
          ),
        ),
      ),
    );
  }
}