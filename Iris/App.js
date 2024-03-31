import { StatusBar } from 'expo-status-bar';
import { Button, StyleSheet, Text, View } from 'react-native';
import { initializeApp } from "firebase/app";
import { getFirestore, collection, addDoc, getDoc, setDoc } from "firebase/firestore";
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

const main = "#C7F2A4";

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

const initRef = doc(db, "init", "test1");
const moduleRef = collection(db, "modules");

const getInfo = async () => {
  const initSnap = await getDoc(initRef);
  return initSnap;
}

const setInfo = async (data) => {
  await setDoc(initRef, {
    Username: data.Username,
    Age: data.Age,
    SpecialNotes: data.SpecialNotes,
    RestrictedWords: data.RestrictedWords,
    SelectedModule: data.SelectedModule
  });
}

const getModules = async () => {
  const moduleSnap = await getDocs(moduleRef);
  return moduleSnap;
}

const addModule = async (data) => {
  await addDoc(moduleRef, {
    Name: data.Name,
    SysInstruction: data.SysInstruction,
    UsrInstruction: data.UsrInstruction
  });
}

export default function App() {
  return (
    <View style={styles.container}>
      <Button title="test" onPress={test} style={styles.button}></Button>
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

  button: {
    borderWidth: 2,
    borderColor: {main},
    borderRadius: 25,
    color: {main},
    textAlign: "center",
    fontSize: 24,
  },
});
