// import React, { useEffect, useState } from 'react';
// import { View, Image, Button } from 'react-native';
// import { database } from '../firebaseconfig';
// import { getDatabase, ref as dataRef, onValue } from "firebase/database";
// import { getStorage, ref as storageRef, getDownloadURL } from "firebase/storage";


// const News = () => {
//   const [imageUrl, setImageUrl] = useState(null);
//   const userId = 'your_user_id'; // Replace with the actual user ID

//   useEffect(() => {
//     // const dbRef = dataRef(getDatabase());
//     // const userRef = dataRef(dbRef, `photolink`);
//     const userRef = dataRef(database, `photolink`);

//     const handleDataChange = (snapshot) => {
//       if (snapshot.exists()) {
//         const data = snapshot.val();
//         const imageLink = data ; // Assuming imageLink is the field containing the image path

//         if (imageLink) {
//           // If the imageLink exists, download the image from Firebase Storage
//           const storage = getStorage();
//           const imageStorageRef = storageRef(storage, imageLink);

//           getDownloadURL(imageStorageRef)
//             .then((url) => {
//               setImageUrl(url);
//             })
//             .catch((error) => {
//               console.error('Error downloading image:', error);
//             });
//         } else {
//           // If the imageLink is not available, you can handle it accordingly
//           setImageUrl(null);
//         }
//       } else {
//         console.log("No data available");
//       }
//     };

//     // Listen for changes in the user's data
//     onValue(userRef, handleDataChange);

//     // Clean up the listener when the component unmounts
//     return () => {
//       off(userRef, 'value', handleDataChange);
//     };
//   }, [userId]);

//   return (
//     <View>
//       {imageUrl ? (
//         <Image source={{ uri: imageUrl }} style={{ width: 200, height: 200 }} />
//       ) : (
//         <View>
//           {/* <Text>No image available</Text> */}
//         </View>
//       )}
      
//       <h3>Please refresh the page to load update</h3>
      
//     </View>

    
      
    
//   );
// };

// export default News;


//////////////////////////////////////////////////////

// import React, { useEffect, useState } from 'react';
// import { View, Image } from 'react-native';
// import { database } from '../firebaseconfig';
// import { ref as dataRef, onValue, off } from 'firebase/database';
// import { getStorage, ref as storageRef, getDownloadURL } from 'firebase/storage';

// const News = () => {
//   const [imageUrl, setImageUrl] = useState(null);
//   const userId = 'your_user_id'; // Replace with the actual user ID

//   useEffect(() => {
//     const userRef = dataRef(database, `photolink`);

//     const handleDataChange = (snapshot) => {
//       if (snapshot.exists()) {
//         setTimeout(() => {
//           const data = snapshot.val();
//           const imageLink = data; // Assuming imageLink is the field containing the image path

//           if (imageLink) {
//             // If the imageLink exists, download the image from Firebase Storage
//             const storage = getStorage();
//             const imageStorageRef = storageRef(storage, imageLink);

//             getDownloadURL(imageStorageRef)
//               .then((url) => {
//                 setImageUrl(url);
//               })
//               .catch((error) => {
//                 console.error('Error downloading image:', error);
//               });
//           } else {
//             // If the imageLink is not available, you can handle it accordingly
//             setImageUrl(null);
//           }
//         }, 5000); // 5000 milliseconds = 5 seconds
//       } else {
//         console.log('No data available');
//       }
//     };

//     // Listen for changes in the user's data
//     onValue(userRef, handleDataChange);

//     // Clean up the listener when the component unmounts
//     return () => {
//       off(userRef, 'value', handleDataChange);
//     };
//   }, [userId]);

//   return (
//     <View>
//       {imageUrl ? (
//         <Image source={{ uri: imageUrl }} style={{ width: 200, height: 200 }} />
//       ) : (
//         <View>
//           {/* <Text>No image available</Text> */}
//         </View>
//       )}

      
//     </View>
//   );
// };

// export default News;





// import React, { useEffect, useState } from 'react';
// import { View, Image, Text } from 'react-native';
// import { database } from '../firebaseconfig';
// import { ref as dataRef, onValue, off } from 'firebase/database';
// import { getStorage, ref as storageRef, getDownloadURL } from 'firebase/storage';

// const News = () => {
//   const [imageUrl, setImageUrl] = useState(null);
//   const userId = 'your_user_id'; // Replace with the actual user ID

//   useEffect(() => {
//     const userRef = dataRef(database, `photolink`);

//     const handleDataChange = (snapshot) => {
//       if (snapshot.exists()) {
//         setTimeout(() => {
//           const data = snapshot.val();
//           const imageLink = data; // Assuming imageLink is the field containing the image path

//           if (imageLink) {
//             // If the imageLink exists, download the image from Firebase Storage
//             const storage = getStorage();
//             const imageStorageRef = storageRef(storage, imageLink);

//             getDownloadURL(imageStorageRef)
//               .then((url) => {
//                 setImageUrl(url);
//               })
//               .catch((error) => {
//                 console.error('Error downloading image:', error);
//               });
//           } else {
//             // If the imageLink is not available, you can handle it accordingly
//             setImageUrl(null);
//           }
//         }, 5000); // 5000 milliseconds = 5 seconds
//       } else {
//         console.log('No data available');
//       }
//     };

//     // Listen for changes in the user's data
//     onValue(userRef, handleDataChange);

//     // Clean up the listener when the component unmounts
//     return () => {
//       off(userRef, 'value', handleDataChange);
//     };
//   }, [userId]);

//   return (
//     <View>
//       {imageUrl ? (
//         <View>
//           <Image source={{ uri: imageUrl }} style={{ width: 200, height: 200 }} />
//           <Text style={{ color: 'red', fontSize: 20 }}>Unauthorized Person is Detected</Text>
//         </View>
//       ) : (
//         <View>
//           {/* <Text>No image available</Text> */}
//         </View>
//       )}

      
//     </View>
//   );
// };

// export default News;



import React, { useEffect, useState } from 'react';
import { View, Image, Text } from 'react-native';
import { database } from '../firebaseconfig';
import { ref as dataRef, onValue, off } from 'firebase/database';
import { getStorage, ref as storageRef, getDownloadURL } from 'firebase/storage';

const News = () => {
  const [imageUrl, setImageUrl] = useState(null);
  const [authority0, setAuthority0] = useState(null); // New state for authority0

  useEffect(() => {
    const userRef = dataRef(database, `authorization`);

    const handleDataChange = (snapshot) => {
      if (snapshot.exists()) {
        setTimeout(() => {
          const data = snapshot.val();
          const imageLink = data.imageLink; // Assuming imageLink is the field containing the image path
          const authorityValue = data.authority; // Assuming authority is the field containing the authorization status

          if (imageLink) {
            // If the imageLink exists, download the image from Firebase Storage
            const storage = getStorage();
            const imageStorageRef = storageRef(storage, imageLink);

            getDownloadURL(imageStorageRef)
              .then((url) => {
                setImageUrl(url);
                setAuthority0(authorityValue);
              })
              .catch((error) => {
                console.error('Error downloading image:', error);
              });
          } else {
            // If the imageLink is not available, you can handle it accordingly
            setImageUrl(null);
            setAuthority0(null);
          }
        }, 5000); // 5000 milliseconds = 3 seconds
      } else {
        console.log('No data available');
      }
    };

    // Listen for changes in the user's data
    onValue(userRef, handleDataChange);

    // Clean up the listener when the component unmounts
    return () => {
      off(userRef, 'value', handleDataChange);
    };
  }, []); // Removed userId from the dependency array as it doesn't seem to be used

  return (
    <View>
      {imageUrl ? (
        <View>
          <Image source={{ uri: imageUrl }} style={{ width: 200, height: 200 }} />
          <Text style={{ color: authority0 === 'dushan' ? 'green' : authority0 === 'mahinda' ? 'green' : authority0 === 'trump' ? 'green' : authority0 === 'accepted1' ? 'green' : authority0 === 'accepted2' ? 'green' : authority0 === 'unknown' ? 'red' : 'red', fontSize: 20 }}>
            {authority0 === 'dushan' ? 'Dushan' : authority0 === 'mahinda' ? 'Mahinda' : authority0 === 'trump' ? 'Trump' : authority0 === 'accepted1' ? 'gave access to enter' : authority0 === 'accepted2' ? 'alarm/lights off--door still has been locked' : authority0 === 'unknown' ? 'Unauthorized person is detected' : ''}
          </Text>
        </View>
      ) : (
        <View>
          {/* <Text>No image available</Text> */}
        </View>
      )}
    </View>
  );
};

export default News;
