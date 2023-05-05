// MovieDetail.js
import React, { useState, useEffect } from 'react';


import {
  View,
  Text,
  Image,
  TouchableOpacity,
  StyleSheet,
  ScrollView,
} from 'react-native';

const MovieDetail = () => {
  const movie = {
    title: 'Movie Title',
    description:
      'This is a description of the movie. It provides an overview of the storyline, characters, and themes.',
    imageUri: 'https://via.placeholder.com/300',
  };

  const watchTrailer = () => {
    // Implement logic to watch the trailer
  };

  const addToFavorites = () => {
    // Implement logic to add the movie to favorites
  };

  const writeReview = () => {
    // Implement logic to write a review
  };

  const shareWithFriends = () => {
    // Implement logic to share the movie with friends
  };

  return (
    <ScrollView style={styles.container}>
      <Image source={{ uri: movie.imageUri }} style={styles.movieImage} />
      <Text style={styles.movieTitle}>{movie.title}</Text>
      <Text style={styles.movieDescription}>{movie.description}</Text>
      <View style={styles.buttonsContainer}>
        <TouchableOpacity style={styles.button} onPress={watchTrailer}>
          <Text style={styles.buttonText}>Watch Trailer</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.button} onPress={addToFavorites}>
          <Text style={styles.buttonText}>Add to Favorites</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.button} onPress={writeReview}>
          <Text style={styles.buttonText}>Write a Review</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.button} onPress={shareWithFriends}>
          <Text style={styles.buttonText}>Share with Friends</Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: 'black',
    paddingHorizontal: 20,
  },
  movieImage: {
    width: '100%',
    height: 300,
    resizeMode: 'cover',
  },
  movieTitle: {
    color: 'white',
    fontSize: 24,
    fontWeight: 'bold',
    marginTop: 20,
    marginBottom: 10,
  },
  movieDescription: {
    color: 'white',
    fontSize: 16,
    marginBottom: 20,
  },
  buttonsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  button: {
    backgroundColor: 'black',
    borderRadius: 5,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 10,
    marginBottom: 15,
    borderColor: 'white',
    borderWidth: 1,
    flexGrow: 1,
    flexBasis: '48%',
  },
  buttonText: {
    color: 'white',
    fontSize: 16,
  },
});

export default MovieDetail;
