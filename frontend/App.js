import React, {useState} from 'react';
import {SafeAreaView, StyleSheet, TextInput, TouchableOpacity, Text, View, Image} from 'react-native';
import {NavigationContainer} from '@react-navigation/native';
import {createStackNavigator} from '@react-navigation/stack';
import Home from './Home';
import Login from './Login';
import Register from './Register';

const App = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [passwordConfirmation, setPasswordConfirmation] = useState('');

  const register = () => {
    // Implement registration logic here
  };


  const Stack = createStackNavigator();
  return (
    <NavigationContainer>
    <Stack.Navigator>
    <Stack.Screen name="Login" component={Login} />
    <Stack.Screen name="Register" component={Register} />
    <Stack.Screen name="Home" component={Home} />
    </Stack.Navigator>
  </NavigationContainer>
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
    height: 40,
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
  buttonText: {
    color: 'white',
    fontSize: 16,
  },
  logo: {
    width: 250,
    height: 250,
    resizeMode: 'contain',
    alignSelf: 'center',
    marginBottom: 15,
  },
});

export default App;
