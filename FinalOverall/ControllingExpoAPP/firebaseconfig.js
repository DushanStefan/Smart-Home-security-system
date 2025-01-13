import { initializeApp } from 'firebase/app';
import { getDatabase } from 'firebase/database';
import { getStorage } from 'firebase/storage';

const firebaseConfig = {
  apiKey: "AIzaSyDVg-GVB75A9q7tixXftyBMvfnAi_7KVDQ",
  authDomain: "realtimeexpo-682c7.firebaseapp.com",
  databaseURL: "https://realtimeexpo-682c7-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "realtimeexpo-682c7",
  storageBucket: "realtimeexpo-682c7.appspot.com",
  messagingSenderId: "854301174342",
  appId: "1:854301174342:web:a39e72ae9022cb2fb53847",
  measurementId: "G-0RKVJTHWNZ"
};
// Initialize Firebase
const app = initializeApp(firebaseConfig);
const database = getDatabase(app);
const storage = getStorage(app);

export { database,storage };
