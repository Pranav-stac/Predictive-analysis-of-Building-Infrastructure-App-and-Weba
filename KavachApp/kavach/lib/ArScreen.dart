import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:arcore_flutter_plugin/arcore_flutter_plugin.dart';
import 'package:image_picker/image_picker.dart';
import 'package:kavach/Home.dart';
import 'package:vector_math/vector_math_64.dart' as vector;

class ArCoreScreen extends StatefulWidget {
  ArCoreScreen({Key? key, required this.title}) : super(key: key);
  final String title;

  @override
  _ArCoreScreenState createState() => _ArCoreScreenState();
}

class _ArCoreScreenState extends State<ArCoreScreen> {
  late ArCoreController arCoreController;
  final ImagePicker _picker = ImagePicker();
  List<Uint8List> images = [];
  List<ArCoreNode> imageNodes = [];

  _onArCoreViewCreated(ArCoreController _arcoreController) {
    arCoreController = _arcoreController;
  }

  Future<void> _pickImage() async {
    final XFile? image = await _picker.pickImage(source: ImageSource.gallery);
    if (image != null) {
      final Uint8List imageBytes = await image.readAsBytes();
      images.add(imageBytes);
      _addImageFrame(arCoreController, imageBytes);
    }
  }

  _addImageFrame(ArCoreController _arcoreController, Uint8List imageBytes) {
    final material = ArCoreMaterial(
      color: Colors.white,
      textureBytes: imageBytes,
    );
    final size = vector.Vector3(1.0, 1.0, 0.01);
    final cube = ArCoreCube(materials: [material], size: size);
    final node = ArCoreNode(
      shape: cube,
      position: vector.Vector3(0, 0, -1.5),
    );

    imageNodes.add(node);
    _arcoreController.addArCoreNode(node);
  }

  void _onSwipe(DragEndDetails details) {
    if (details.primaryVelocity != null) {
      if (details.primaryVelocity! > 0) {
        // Swipe right
        // Implement logic to handle swipe right
      } else if (details.primaryVelocity! < 0) {
        // Swipe left
        // Add a new image node on swipe left using the last loaded image
        _addImageFrame(arCoreController, images.last);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title),
      ),
      body: GestureDetector(
        onHorizontalDragEnd: _onSwipe,
        child: ArCoreView(
          onArCoreViewCreated: _onArCoreViewCreated,
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _pickImage,
        tooltip: 'Pick Image',
        child: Icon(Icons.photo_library),
      ),
      floatingActionButtonLocation: FloatingActionButtonLocation.endFloat,
      persistentFooterButtons: [
        ElevatedButton(
          onPressed: () {
        Navigator.push(
          context,
          MaterialPageRoute(builder: (context) => HomePage()),
        );
          },
          child: Text('Go to Home Screen'),
        ),
      ],
    );
  }

  @override
  void dispose() {
    arCoreController.dispose();
    super.dispose();
  }
}

