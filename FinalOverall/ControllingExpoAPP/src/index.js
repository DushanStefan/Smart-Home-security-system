import { View, Text, StyleSheet, Button } from 'react-native';
import React, { useState } from 'react';
import { database } from '../firebaseconfig';
import { ref as databaseRef,update } from 'firebase/database'; // Rename 'ref' to 'dbRef'


const FetchData = () => {
  const [light, setLight] = useState(false);
  const [lock, setLock] = useState(false);
  const [imageUrl, setImageUrl] = useState('');

//   const dbRef2 = databaseRef(database);
//   const db = getDatabase();
//   const starCountRef = ref(db, 'photolink');

//   const storage = getStorage();
//   let imageRef;
  
//   // get(child(dbRef2, 'photolink'))
//   //     .then((snapshot) => {
//   onValue(starCountRef, (snapshot) => {
//         if (snapshot.exists() && snapshot.val()=="ert.jpg") {
//           console.log("the rog the rig");
//           console.log(snapshot.val());
//           imageRef = storageRef(storage, 'ert.jpg');}
//         else{
//           imageRef = storageRef(storage, 'good.png');}

//         getDownloadURL(imageRef); // Return the promise for chaining
//         })

//       // .then((url) => {
//       //   setImageUrl(url);
//       //   })

//       // .catch((error) => {
//       //   console.error(error);
//       //   });

//   getDownloadURL(imageRef)
//     .then((url) => {
//       setImageUrl(url);
//     })
//     .catch((error) => {
//       console.error(error);
//     });

  const updateData = (field) => {
    const dbRef = databaseRef(database); // Use 'dbRef' instead of 'ref'

    update(dbRef, field);
  };

  const handleSetLight = () => {
    updateData({ light: 'off' });
    setLight('off');
  };

  const handleSetLock = () => {
    updateData({ lock: 'unlock' });
    setLock('unlock');
  };

  return (
    <View style={styles.container}>
      {/* <h1>Safe_Home</h1> */}
      {/* {imageUrl && <Image source={{ uri: imageUrl }} style={{ width: 200, height: 200 }} />} */}
      <Button title="Off lights & alarms" onPress={handleSetLight} />
      <Button
        title="Off lights & alarms + unlock door"
        onPress={() => {
          handleSetLock();
          handleSetLight();
        }}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
});

export default FetchData;
