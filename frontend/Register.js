import React, {useState} from 'react';
import {SafeAreaView, StyleSheet, TextInput, TouchableOpacity, Text, View, Image} from 'react-native';
import {NavigationContainer} from '@react-navigation/native';
import {createStackNavigator} from '@react-navigation/stack';
import Home from './Home';
import MovieDetail from './MovieDetail';
import { signUpWithEmail } from './Firebase';


const Register = ({ navigation }) => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [passwordConfirmation, setPasswordConfirmation] = useState('');

  const register = () => {

    var raw = {
      "id": fnv32a(username),
      "name": username,
      "email": email,
      "avatar": fnv32a(email),
      "password": password
    }

    var requestOptions = {
      method: 'POST',
      body: JSON.stringify(raw),
      redirect: 'follow'
    };
    signUpWithEmail(username, email, password)
      .then(() => {
        console.log("Firebase: User Auth register SUCCESS")
      })
      .catch((error) => {
        console.log("Firebase: User Auth register FAIL")
      });



    fetch("http://127.0.0.1:5/oauthuser", requestOptions)
      .then(response => response.text())
      .then(result => {
        console.log(result);
        if (JSON.parse(result)["success"]) {
          console.log("Register Successful")
          navigation.navigate('Home');
        }
      })
      .catch(error => console.log('error', error));
  };
function fnv32a(str) {
  let hash = 0x811c9dc5;

  for (let i = 0; i < str.length; i++) {
    hash ^= str.charCodeAt(i);
    hash += (hash << 1) + (hash << 4) + (hash << 7) + (hash << 8) + (hash << 24);
  }

  return hash >>> 0; // Use unsigned right shift to convert to a positive integer
}


  const Stack = createStackNavigator();
  const handleRegister = () => {
    navigation.navigate("Login");
  };
  const handleMovieDetail = () => {
    navigation.navigate('MovieDetail');
  };
  return (
    <SafeAreaView style={styles.container}>
      <Image source={require('./Rectangle5.png')} style={styles.logo} />
      <View style={styles.form}>
        <Text style={styles.label}>Username</Text>
        <TextInput
          style={styles.input}
          onChangeText={setUsername}
          value={username}
          placeholder="Enter your username"
        />

        <Text style={styles.label}>Email</Text>
        <TextInput
          style={styles.input}
          onChangeText={setEmail}
          value={email}
          placeholder="Enter your email"
          keyboardType="email-address"
        />

        <Text style={styles.label}>Password</Text>
        <TextInput
          style={styles.input}
          onChangeText={setPassword}
          value={password}
          placeholder="Enter your password"
          secureTextEntry
        />

        <Text style={styles.label}>Confirm Password</Text>
        <TextInput
          style={styles.input}
          onChangeText={setPasswordConfirmation}
          value={passwordConfirmation}
          placeholder="Confirm your password"
          secureTextEntry
        />

        <TouchableOpacity style={styles.button} onPress={register}>
          <Text style={styles.buttonText}>Register</Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.altbutton} onPress={handleRegister}>
          <Text style={styles.buttonText}>Have an account? </Text>
        </ TouchableOpacity>
      </View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: 'black',
    justifyContent: 'center',
  },
  form: {
    paddingHorizontal: 20,
  },
  label: {
    color: 'white',
    fontSize: 16,
    marginLeft: 4,
  },
  input: {
    height: 30,
    backgroundColor: 'white',
    paddingHorizontal: 10,
    marginBottom: 15,
    borderRadius: 50,
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
  },
  altbutton: {
    backgroundColor: 'black',
    borderRadius: 5,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 10,
    marginBottom: 15,

  },
  buttonText: {
    color: 'white',
    fontSize: 16,
  },
  logo: {
    width: 250,
    height: 250,
    resizeMode: 'contain',
    alignSelf: 'center',
    marginBottom: 0,
  },
});

export default Register;
