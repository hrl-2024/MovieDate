// Home.js
import React, { useState } from 'react';
import {
  View,
  Text,
  Image,
  TextInput,
  FlatList,
  StyleSheet,
} from 'react-native';

const data = [
  { id: '1', uri: 'https://posters.movieposterdb.com/10_06/2010/1375666/s_1375666_07030c72.jpg'},
  { id: '1', uri: 'https://posters.movieposterdb.com/23_01/2010/1790736/s_inception-the-cobol-job-movie-poster_15eafd4a.jpg'},
  { id: '1', uri: 'https://posters.movieposterdb.com/23_02/2014/7321322/l_inception-movie-poster_871102ec.jpg'},
  { id: '1', uri: 'https://posters.movieposterdb.com/19_12/2015/8269586/s_8269586_8a44c5d4.jpg'},
  { id: '1', uri: 'https://posters.movieposterdb.com/23_02/2014/5735302/s_starlight-inception-movie-poster_019fe54e.jpg'},
  // Add your image sources here, for example:
  // { id: '1', uri: 'https://via.placeholder.com/150' },
  // { id: '2', uri: 'https://via.placeholder.com/150' },
  // ...
];

const renderItem = ({ item }) => (
  <Image source={{ uri: item.uri }} style={styles.galleryImage} />
);

const Home = () => {
  const [search, setSearch] = useState('');

  return (
    <View style={styles.container}>
      <Image
        source={require('./Rectangle5.png')} // Replace with the path to your logo image file
        style={styles.logo}
      />
      <TextInput
        style={styles.searchBar}
        onChangeText={(text) => setSearch(text)}
        value={search}
        placeholder="Search"
        placeholderTextColor="white"
      />
      <FlatList
        data={data}
        renderItem={renderItem}
        keyExtractor={(item) => item.id}
        horizontal
        showsHorizontalScrollIndicator={false}
        contentContainerStyle={styles.gallery}
      />
      <FlatList
        data={data}
        renderItem={renderItem}
        keyExtractor={(item) => item.id}
        horizontal
        showsHorizontalScrollIndicator={false}
        contentContainerStyle={styles.gallery}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#000',
  },
  logo: {
    width: 150,
    height: 150,
    resizeMode: 'contain',
    alignSelf: 'center',
    marginBottom: 20,
  },
  searchBar: {
    width: '80%',
    height: 40,
    backgroundColor: 'white',
    borderRadius: 25,
    paddingHorizontal: 15,
    marginBottom: 20,
    color: 'black',
  },
  gallery: {
    paddingHorizontal: 10,
  },
  galleryImage: {
    width: 150,
    height: 150,
    marginRight: 10,
  },
});

export default Home;
