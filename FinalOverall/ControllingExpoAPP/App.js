import { StyleSheet, View } from 'react-native';
import FetchData from './src/index';
import News from './src/new';

export default function App() {
  return (
    <View style={styles.container}>
      <FetchData/>
      <News/>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#87CEEB',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
