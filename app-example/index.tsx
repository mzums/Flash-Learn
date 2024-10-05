import { Text, View, /* @tutinfo Import <CODE>StyleSheet</CODE> to define styles. */ StyleSheet } from 'react-native';

export default function Index() {
  return (
    <View style={styles.container}>
      /* @tutinfo This used to say "Edit app/index.tsx to edit this screen". Now it says, "Home screen". */
      <Text style={styles.text}>Home screen</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    /* @tutinfo Add the value of <CODE>backgroundColor</CODE> property with <CODE>'#25292e'</CODE>.*/
    backgroundColor: '#25292e',
    alignItems: 'center',
    justifyContent: 'center',
  },
  text: {
    color: '#fff',
  },
});
