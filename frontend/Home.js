// Home.js
import React, { useState, useEffect } from 'react';

import {
  View,
  Text,
  Image,
  TextInput,
  FlatList,
  StyleSheet,
} from 'react-native';

const data = [];

const renderItem = ({ item }) => (
  <Image source={{ uri: item.uri }} style={styles.galleryImage} />
);

const Home = () => {
  const [token, setToken] = useState('');
  const [movieData, setMovieData] = useState({});

  useEffect(() => {
    fetch("http://127.0.0.1:5/gettoken")
      .then(response => response.text())
      .then(result => {
        console.log(JSON.parse(result)["token"]);
        setToken(JSON.parse(result)["token"])
      })
      .catch(error => console.log('error', error));
  }, []);

  useEffect(() => {
    if (token) {
      fetch(`https://api.themoviedb.org/3/movie/popular?api_key=${token}&language=en-US&page=1`)
      .then(response => response.json())
      .then(data => {
        console.log(data);
        setMovieData(data)
      })
      .catch(error => console.error(error));
    }
  },[])
  console.log(movieData)
  for (let movie in movieData["results"]) {
    data.push({id: `${movieData["id"]}`, uri: `https://image.tmdb.org/t/p/w500/${movie["backdrop_path"]}`})
    console.log(`https://image.tmdb.org/t/p/w500/${movie["backdrop_path"]}`)
  }
  console.log("EMMMME")
  console.log(data)

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
