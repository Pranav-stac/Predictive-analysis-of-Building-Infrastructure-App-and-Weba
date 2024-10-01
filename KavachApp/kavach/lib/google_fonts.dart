import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart'; // Add this import
import 'dart:convert'; // Add this import
import 'package:flutter/services.dart' show rootBundle; // Add this import
import 'dart:math'; // Add this import

class Heatmap extends StatefulWidget { // Change to StatefulWidget
  @override
  _HeatmapState createState() => _HeatmapState();
}

class _HeatmapState extends State<Heatmap> {
  final ImagePicker _picker = ImagePicker();
  XFile? _image;
  GoogleMapController? _mapController;
  List<Circle> _circles = [];
  List<dynamic> _data = []; // Store JSON data

  @override
  void initState() {
    super.initState();
    _loadJsonData();
  }

  Future<void> _loadJsonData() async {
    final String response = await rootBundle.loadString('assets/output.json');
    final data = await json.decode(response);
    setState(() {
      _data = data; // Store the data
      _circles = _createCircles(data, Colors.yellow); // Use yellow circles for heat by default
    });
  }

  List<Circle> _createCircles(List<dynamic> data, Color color) {
    List<Circle> circles = [];
    Random random = Random();
    for (int i = 0; i < data.length; i++) {
      if (random.nextBool()) { // Randomly decide to add circle
        circles.add(
          Circle(
            circleId: CircleId(i.toString()),
            center: LatLng(
              double.parse(data[i]['latitude']),
              double.parse(data[i]['longitude']),
            ),
            radius: 70000, // Radius in meters
            fillColor: color.withOpacity(0.5),
            strokeColor: color,
            strokeWidth: 1,
          ),
        );
      }
    }
    return circles;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Weather Analysis on Public Infrastructure'),
        backgroundColor: Color(0xFF1a1a2e),
      ),
      body: SingleChildScrollView(
        child: Column(
          children: [
            _buildNavBar(),
            _buildHomeSection(),
            _buildWeatherAnalysisSection(context),
          ],
        ),
      ),
    );
  }

  Widget _buildNavBar() {
    return Container(
      color: Color(0xFF1a1a2e),
      padding: EdgeInsets.symmetric(vertical: 0, horizontal: 12),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Row(
            children: [
              Image.network(
                'https://i.postimg.cc/x1798YMx/image.png',
                width: 60,
              ),
              SizedBox(width: 16),
              Text(
                'Kavach',
                style: TextStyle(
                  color: Color(0xFFe94560),
                  fontSize: 24,
                ),
              ),
            ],
          ),
          Row(
            children: [
              _buildNavItem('Home'),
              SizedBox(width: 16),
              _buildNavItem('Contact'),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildNavItem(String title) {
    return Text(
      title,
      style: TextStyle(
        color: Color(0xFFe94560),
        fontSize: 18,
      ),
    );
  }

  Widget _buildHomeSection() {
    return Container(
      color: Color(0xFF16213e),
      padding: EdgeInsets.symmetric(vertical: 32, horizontal: 10),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Weather Analysis on Public Infrastructure',
            style: TextStyle(
              color: Color(0xFFe94560),
              fontSize: 28,
            ),
          ),
          SizedBox(height: 16),
          Text(
            'Analyze the impact of weather on public infrastructure.',
            style: TextStyle(
              color: Colors.white,
              fontSize: 18,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildWeatherAnalysisSection(BuildContext context) {
    return Container(
      padding: EdgeInsets.all(16),
      child: Column(
        children: [
          Container(
            height: 300,
            child: GoogleMap(
              onMapCreated: (GoogleMapController controller) {
                _mapController = controller;
              },
              initialCameraPosition: CameraPosition(
                target: LatLng(20.5937, 78.9629),
                zoom: 5,
              ),
              circles: Set<Circle>.of(_circles), // Add circles to the map
            ),
          ),
          SizedBox(height: 16),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: [
              Expanded(
                child: ElevatedButton(
                  onPressed: () {
                    setState(() {
                      _circles = _createCircles(_data, Colors.yellow); // Yellow circles for heat
                    });
                  },
                  child: Text('Heat'),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Color(0xFFe94560),
                    foregroundColor: Colors.white,
                  ),
                ),
              ),
              SizedBox(width: 16),
              Expanded(
                child: ElevatedButton(
                  onPressed: () {
                    setState(() {
                      _circles = _createCircles(_data, Colors.blue); // Blue circles for rain
                    });
                  },
                  child: Text('Rain'),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Color(0xFFe94560),
                    foregroundColor: Colors.white,
                  ),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  void _showTitleDialog(BuildContext context) {
    TextEditingController _titleController = TextEditingController();
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: Text('Enter Title'),
          content: TextField(
            controller: _titleController,
            decoration: InputDecoration(hintText: "Title"),
          ),
          actions: [
            ElevatedButton(
              onPressed: () {
                // Call your API with _image and _titleController.text
                Navigator.of(context).pop();
              },
              child: Text('Generate Report'),
            ),
          ],
        );
      },
    );
  }
}