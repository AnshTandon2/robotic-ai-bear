import { StatusBar } from 'expo-status-bar';
import { Button, StyleSheet, Text, View } from 'react-native';
import { initializeApp } from "firebase/app";
import { getFirestore, collection, addDoc } from "firebase/firestore";
// Import the functions you need from the SDKs you need
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyDBuPmeoud8m_00BlNSLuXXav625KGD1_I",
  authDomain: "iris-49575.firebaseapp.com",
  databaseURL: "https://iris-49575-default-rtdb.firebaseio.com",
  projectId: "iris-49575",
  storageBucket: "iris-49575.appspot.com",
  messagingSenderId: "543402325380",
  appId: "1:543402325380:web:7636d852b2e7534de7d9d1",
  measurementId: "G-8FKQTK3R78"
};

// Initialize Firebase
const test = async () => {
  try {
    const docRef = await addDoc(collection(db, "users"), {
      first: "Ada",
      last: "Lovelace",
      born: 1815
    });
    console.log("Document written with ID: ", docRef.id);
  } catch (e) {
    console.error("Error adding document: ", e);
  }
};

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

export default function App() {
  return (
    <View style={styles.container}>
      <Button title="test" onPress={test}></Button>
      <Text>Open up App.js to start working on your app!</Text>
      <StatusBar style="auto" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
