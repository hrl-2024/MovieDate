// Register.js
import React, {useState} from 'react';
import {StyleSheet, TextInput, TouchableOpacity, Text, View, Image} from 'react-native';

const Register = ({navigation}) => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [passwordConfirmation, setPasswordConfirmation] = useState('');

  const register = () => {
    
    var raw = "{\n    \"name\": \”Andrew\”,\n    \"avatar\": 1234234235\n}";

    var requestOptions = {
      method: 'POST',
      body: raw,
      redirect: 'follow'
    };

    fetch("http://127.0.0.1:5002/user", requestOptions)
      .then(response => response.text())
      .then(result => console.log(result))
      .catch(error => console.log('error', error));
};

  const login = () => {
    // Implement login logic here
    navigation.navigate('Home');
  };
  

  return (
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

        <TouchableOpacity style={styles.button} onPress={login}>
          <Text style={styles.buttonText}>Login</Text>
        </ TouchableOpacity>
      </View>
  );
};

// Styles object

export default Register;
