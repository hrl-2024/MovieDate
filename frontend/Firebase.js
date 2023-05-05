// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";

import { GoogleAuthProvider, getAuth, signInWithEmailAndPassword, createUserWithEmailAndPassword, updateProfile } from "firebase/auth";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyBOZkJ3SPGJYV1wMowty7VLBlfc_QN1ymA",
  authDomain: "cs411-project-c05a5.firebaseapp.com",
  projectId: "cs411-project-c05a5",
  storageBucket: "cs411-project-c05a5.appspot.com",
  messagingSenderId: "761934558512",
  appId: "1:761934558512:web:7ceb3c1acf19fa323ac4f5",
  measurementId: "G-579BWG8Y28"
};

// Initialize Firebase
export const app = initializeApp(firebaseConfig);
export const auth = getAuth();

const provider = new GoogleAuthProvider()

export const signUpWithEmail = (username, email, password) => {
    return createUserWithEmailAndPassword(auth, email, password)
      .then((userCredential) => {
        // Update the user's display name
        const user = userCredential.user;
        return updateProfile(user, { displayName: username });
      })
      .catch((error) => {
        const errorCode = error.code;
        const errorMessage = error.message;
        console.log(errorCode, errorMessage);
        throw new Error(errorMessage);
      });
  }

export const signInWithEmail = (email, password) => {
  return signInWithEmailAndPassword(auth, email, password)
    .then((userCredential) => {
      // Signed in
      const user = userCredential.user;
      console.log(user);
    })
    .catch((error) => {
      const errorCode = error.code;
      const errorMessage = error.message;
      console.log(errorCode, errorMessage);
    });
}



  