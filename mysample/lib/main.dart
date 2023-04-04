import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

void main() => runApp(const CupertinoTabBarApp());

class CupertinoTabBarApp extends StatelessWidget {
  const CupertinoTabBarApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const CupertinoApp(
      theme: CupertinoThemeData(brightness: Brightness.dark),
      home: CupertinoTabBarExample(),
    );
  }
}

class CupertinoTabBarExample extends StatelessWidget {
  const CupertinoTabBarExample({super.key});

  @override
  Widget build(BuildContext context) {
    return CupertinoTabScaffold(
      tabBar: CupertinoTabBar(
        items: const <BottomNavigationBarItem>[
          BottomNavigationBarItem(
            icon: Icon(CupertinoIcons.film),
            label: 'Movie',
          ),
          BottomNavigationBarItem(
            icon: Icon(CupertinoIcons.chat_bubble_2),
            label: 'Chat',
          ),
          BottomNavigationBarItem(
            icon: Icon(CupertinoIcons.group),
            label: 'Community',
          ),
          BottomNavigationBarItem(
            icon: Icon(CupertinoIcons.person),
            label: 'Profile',
          ),
        ],
      ),
      tabBuilder: (BuildContext context, int index) {
        return CupertinoTabView(
          builder: (BuildContext context) {
            return HomePage();
          },
        );
      },
    );
  }
}

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _MovieHomePage();
}

class _MovieHomePage extends State<HomePage> {
  late TextEditingController textController;

  @override
  void initState() {
    super.initState();
    textController = TextEditingController(text: '');
  }

  @override
  void dispose() {
    textController.dispose();
    super.dispose();
  }

  // @override
  // Widget build(BuildContext context) {
  //   return CupertinoPageScaffold(
  //     navigationBar: const CupertinoNavigationBar(
  //       middle: Image(image: AssetImage('assets/MovieDate_logo.png'), width: 200),
  //     ),
  //     child: Center(
  //       child: Padding(
  //         padding: const EdgeInsets.all(16.0),
  //         child: CupertinoSearchTextField(
  //           controller: textController,
  //           placeholder: 'Search',
  //         ),
  //       ),
  //     ),
  //   );
  // }

  @override
  Widget build(BuildContext context) {  
    return Column(
      crossAxisAlignment: CrossAxisAlignment.center,

      children: [
        LayoutBuilder(
          builder: (context, constraints) {
            return Column(
              children: [
                const SizedBox(height: 40),
                Image(image: const AssetImage('assets/MovieDate_logo.png'), width: constraints.maxWidth / 2),

                const SizedBox(height: 40),

                // Search bar:
                SizedBox(width: constraints.maxWidth - 10, child: CupertinoSearchTextField(
                    controller: textController,
                    placeholder: 'Search for a movie',

                    itemColor: Colors.grey,

                    decoration: BoxDecoration(
                      color: Colors.white,
                      border: Border.all(
                        width: 0,
                      ),
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                )
              ],
            );
          }
        )
      ],
    );
  }
}