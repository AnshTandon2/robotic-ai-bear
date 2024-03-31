import 'bootstrap/dist/css/bootstrap.min.css';
import { StatusBar } from 'expo-status-bar';
import { useState } from 'react';
import { NativeBaseProvider, Container, extendTheme } from 'native-base';
import { Button, Pressable, StyleSheet, Text, View } from 'react-native';
import { initializeApp } from "firebase/app";
import { getFirestore, collection, addDoc, getDoc, setDoc } from "firebase/firestore";
// Import the functions you need from the SDKs you need
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const main = "#379237";
const secondary = "#C7F2A4";

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

const config = {
  useSystemColorMode: false,
  initialColorMode: secondary,
};

// extend the theme
const customTheme = extendTheme({ config });


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

const change = (tab) => {
  switch (tab) {
    case 'home':
      console.log("home select");
      return;
    case 'colors':
      console.log("home select");
      return;
    case 'modules':
      console.log("home select");
      return;
    default:
      return;
  }
  //const main = document.getElementById("main");

  //main.innerHTML = {}
}

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);
//const [tab, setTab] = useState('home');

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
  const [tab, setTab] = useState('home');

  return (
    <NativeBaseProvider theme={customTheme}>
      <View style={{
        flex: 1,
        flexDirection: 'row',
        justifyContent: 'center',
        alignItems: 'flex-end'
      }}>
        <View>
          <Pressable title='' style={styles.tab} onPress={() => {setTab('home'),
            change(tab)}}>
            <Text style={styles.text}>Home</Text>
          </Pressable>
        </View>
        <View>
          <Pressable title='' style={styles.tab} onPress={() => {setTab('colors'),
            change(tab)}}>
            <Text style={styles.text}>Colors</Text>
          </Pressable>
        </View>
        <View>
          <Pressable title='' style={styles.tab} onPress={() => {setTab('modules'),
            change(tab)}}>
            <Text style={styles.text}>Modules</Text>
          </Pressable>
        </View>
      </View>
      
    </NativeBaseProvider>
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
    alignItems: 'center',
    borderWidth: 2,
    borderColor: main,
    justifyContent: 'center',
    borderRadius: 18,
    shadowColor: secondary,
    shadowRadius: 2,
    shadowOffset: {width: 0, height: 0},
    shadowOpacity: 1,
    paddingVertical: 12,
    paddingHorizontal: 32,
  },

  tab: {
    height: 100,
    borderWidth: 2,
    borderColor: main,
    borderRadius: 18,
    shadowColor: secondary,
    shadowRadius: 2,
    shadowOffset: {width: 0, height: 0},
    shadowOpacity: 1,
    paddingVertical: -10,
    paddingHorizontal: 32,
    margin: 1,
    justifyContent: 'center',
    //position: 'absolute',
  },
  text: {
    color: main,
    fontSize: 12,
    fontFamily: "Verdana",
    fontWeight: "bold",
  }
});
