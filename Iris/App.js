import 'bootstrap/dist/css/bootstrap.min.css';
import { StatusBar } from 'expo-status-bar';
import { useState, useRef } from 'react';
import { NativeBaseProvider, Container, extendTheme } from 'native-base';
import { Button, Pressable, StyleSheet, Text, View } from 'react-native';
import { initializeApp } from "firebase/app";
import { getFirestore, collection, addDoc, getDoc, setDoc, doc } from "firebase/firestore";
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

// Initialize Firebase

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
  const [txt, setTxt] = useState("Test");

  return (
    <NativeBaseProvider style={styles.container}>
      <View style={{
        height: "100%",
        width: "auto",
        backgroundColor: "#fff",
        alignItems: "center",
        justifyContent: "center"
      }}>
        <Text style={{
          fontFamily: "Verdana",
          fontWeight: "bold"
        }}>{txt}</Text>
      </View>

      <View style={{
        flex: 1,
        flexDirection: 'row',
        justifyContent: 'space-evenly',
        alignItems: 'center',
        backgroundColor: secondary,
        bottom: 50, 
        width: '90%',
        alignSelf: "center",
        alignContent: "center",
        borderRadius: 18,
        shadowColor: 'black',
        shadowOffset: {width: 0, height: 1},
        shadowOpacity: 0.2,
        shadowRadius: 2,
        position: "absolute" 
      }}>
        <View>
          <Pressable title='' style={styles.tab} onPress={() => {setTxt('home')}}>
            <Text style={styles.text}>Home</Text>
          </Pressable>
        </View>
        <View>
          <Pressable title='' style={styles.tab} onPress={() => {setTxt("info")}}>
            <Text style={styles.text}>Info</Text>
          </Pressable>
        </View>
        <View>
          <Pressable title='' style={styles.tab} onPress={() => {setTxt('modules')}}>
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
    backgroundColor: "#fff",
    alignItems: 'center',
    justifyContent: 'center',
  },

  button: {
    alignItems: 'center',
    borderWidth: 2,
    borderColor: main,
    justifyContent: 'center',
    borderRadius: 18,
    shadowColor: main,
    shadowRadius: 4,
    shadowOffset: {width: 0, height: 0},
    shadowOpacity: 1,
    paddingVertical: 12,
    paddingHorizontal: 32,
  },

  tab: {
    borderWidth: 2,
    borderColor: main,
    borderRadius: 18,
    shadowColor: main,
    shadowRadius: 8,
    shadowOffset: {width: 0, height: 0},
    shadowOpacity: 1,
    paddingVertical: 15,
    paddingHorizontal: 20,
    margin: 10,
    width: 100,
    justifyContent: 'center',
    alignItems: 'center',
    //position: 'absolute',
  },
  text: {
    color: "#fff",
    fontSize: 12,
    fontFamily: "Verdana",
    fontWeight: "bold",
    padding: 0,
  }
});
