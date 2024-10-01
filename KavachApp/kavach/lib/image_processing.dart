import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:geolocator/geolocator.dart'; // Add this import
import 'dart:io';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(MaterialApp(
    home: MonitoringRoadsPage(),
  ));
}

class MonitoringRoadsPage extends StatefulWidget {
  @override
  _MonitoringRoadsPageState createState() => _MonitoringRoadsPageState();
}

class _MonitoringRoadsPageState extends State<MonitoringRoadsPage> {
  final ImagePicker _picker = ImagePicker();
  XFile? _image;
  final TextEditingController _titleController = TextEditingController();
  final TextEditingController _descriptionController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Monitoring Roads'),
        backgroundColor: Color(0xFF1a1a2e),
      ),
      body: SingleChildScrollView(
        child: Column(
          children: [
            _buildNavBar(),
            _buildHomeSection(),
            _buildMonitoringRoadsSection(context),
          ],
        ),
      ),
    );
  }

  Widget _buildNavBar() {
    return Container(
      color: Color(0xFF1a1a2e),
      padding: EdgeInsets.symmetric(vertical: 16, horizontal: 32),
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
      padding: EdgeInsets.symmetric(vertical: 32, horizontal: 64),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Monitoring Roads',
            style: TextStyle(
              color: Color(0xFFe94560),
              fontSize: 28,
            ),
          ),
          SizedBox(height: 16),
          Text(
            'Monitor roads based on traffic usage and maintenance records.',
            style: TextStyle(
              color: Colors.white,
              fontSize: 18,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildMonitoringRoadsSection(BuildContext context) {
    return Container(
      padding: EdgeInsets.all(16),
      child: Column(
        children: [
          Container(
            height: 300,
            color: Colors.grey[300],
            child: Center(
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  ElevatedButton(
                    onPressed: () async {
                      _image = await _picker.pickImage(source: ImageSource.camera);
                      if (_image != null) {
                        _showTitleDialog(context);
                      }
                    },
                    child: Row(
                      children: [
                        Icon(Icons.camera_alt),
                        SizedBox(width: 8),
                        Text('Start Camera'),
                      ],
                    ),
                  ),
                  SizedBox(width: 16),
                  ElevatedButton(
                    onPressed: () async {
                      _image = await _picker.pickImage(source: ImageSource.gallery);
                      if (_image != null) {
                        _showTitleDialog(context);
                      }
                    },
                    child: Row(
                      children: [
                        Icon(Icons.photo_library),
                        SizedBox(width: 8),
                        Text('Pick from Gallery'),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  void _showTitleDialog(BuildContext context) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: Text('Enter Details'),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              TextField(
                controller: _titleController,
                decoration: InputDecoration(labelText: 'Title'),
              ),
              TextField(
                controller: _descriptionController,
                decoration: InputDecoration(labelText: 'Description'),
              ),
            ],
          ),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.of(context).pop();
              },
              child: Text('Cancel'),
            ),
            TextButton(
              onPressed: () async {
                Position position = await _determinePosition();
                await uploadComplaint(
                  _titleController.text,
                  _descriptionController.text,
                  _image!.path,
                  position.latitude,
                  position.longitude,
                );
                Navigator.of(context).pop();
              },
              child: Text('Submit'),
            ),
          ],
        );
      },
    );
  }

  Future<Position> _determinePosition() async {
    bool serviceEnabled;
    LocationPermission permission;

    // Test if location services are enabled.
    serviceEnabled = await Geolocator.isLocationServiceEnabled();
    if (!serviceEnabled) {
      return Future.error('Location services are disabled.');
    }

    permission = await Geolocator.checkPermission();
    if (permission == LocationPermission.denied) {
      permission = await Geolocator.requestPermission();
      if (permission == LocationPermission.denied) {
        return Future.error('Location permissions are denied');
      }
    }

    if (permission == LocationPermission.deniedForever) {
      return Future.error(
          'Location permissions are permanently denied, we cannot request permissions.');
    }

    return await Geolocator.getCurrentPosition();
  }

  Future<void> uploadComplaint(String title, String description, String imagePath, double latitude, double longitude) async {
    final Uri apiUrl = Uri.parse('https://cheerful-apparent-hound.ngrok-free.app/upload-complaint/'); // Replace with your API URL

    // Prepare the request
    var request = http.MultipartRequest('POST', apiUrl)
      ..fields['title'] = title
      ..fields['description'] = description
      ..fields['latitude'] = latitude.toString()
      ..fields['longitude'] = longitude.toString();

    // Add the image file
    if (imagePath.isNotEmpty) {
      var imageFile = await http.MultipartFile.fromPath('image', imagePath);
      request.files.add(imageFile);
    }

    // Send the request
    try {
      var response = await request.send();
      if (response.statusCode == 201) {
        // Successfully uploaded
        print('Complaint uploaded successfully');
        var responseData = await response.stream.toBytes();
        var responseString = String.fromCharCodes(responseData);
        print('Response: $responseString');
      } else {
        // Handle error
        print('Failed to upload complaint: ${response.statusCode}');
      }
    } catch (e) {
      print('Error: $e');
    }
  }
}