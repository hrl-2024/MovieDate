import React, {useState} from 'react';
import {SafeAreaView, StyleSheet, TextInput, TouchableOpacity, Text, View, Image} from 'react-native';
import {NavigationContainer} from '@react-navigation/native';
import {createStackNavigator} from '@react-navigation/stack';
import Home from './Home';
import MovieDetail from './MovieDetail';
import { getAuth, signInWithEmailAndPassword } from "firebase/auth";
import { signInWithEmail } from "./Firebase";
import { Alert } from 'react-native';
const Login = ({navigation}) => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const login = () => {
    
    var raw = {
    "name": username,
    "email": email,
    "password": password
}

    var requestOptions = {
      method: 'POST', 
      body: JSON.stringify(raw),
      redirect: 'follow'
    };
    signInWithEmail(email, password)
      .then((user) => {
        console.log("Firebase: User Auth login SUCCESS");
        navigation.navigate('Home');
      })
      .catch((error) => {
        console.log("Firebase: User Auth login FAIL", error);
        Alert.alert(
          'Error',
          'Invalid Login Details.',
          [
            {
              text: 'OK',
              onPress: () => console.log('OK pressed'),
            },
          ],
          { cancelable: false }
        );
        console.error(error);
      });

      fetch("http://127.0.0.1:5002/user", requestOptions)
      .then(response => response.text())
      .then(result => {
        console.log("bing",result);
        if (JSON.parse(result)["success"]) {
          navigation.navigate('Home');
          console.log("Login Successful")
        }
      })
      .catch(error => console.log('error', error));
      


};



  const Stack = createStackNavigator();
  const handleLogin = () => {
    navigation.navigate('Register');
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

        <TouchableOpacity style={styles.button} onPress={login}>
          <Text style={styles.buttonText}>Login</Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.altbutton} onPress={handleLogin}>
          <Text style={styles.buttonText}>Create an account</Text>
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

export default Login;
