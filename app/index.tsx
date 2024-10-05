import React, { useState } from 'react';
import { Button, View, Text, StyleSheet } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';

// Typy dla nawigacji
type RootStackParamList = {
  Home: undefined;
  Details: undefined;
};

type HomeScreenProps = {
  navigation: NativeStackNavigationProp<RootStackParamList, 'Home'>;
};

const Stack = createNativeStackNavigator<RootStackParamList>();

const HomeScreen: React.FC<HomeScreenProps> = ({ navigation }) => {
  const [howMany, setHowMany] = useState(3); // Przykładowa wartość

  const _onPressButton = () => {
    console.log("Button pressed!");
  };

  const _onPressPlus = () => {
    setHowMany(prev => prev + 1);
  };

  return (
    <View style={styles.container}>
      {/* Generowanie przycisków w oparciu o wartość howMany ze stanu */}
      {Array.from({ length: howMany }).map((_, index) => (
        <View style={styles.buttonContainer} key={index}>
          <Button onPress={_onPressButton} title={`Press Me ${index + 1}`} />
        </View>
      ))}
      <View style={styles.alternativeLayoutButtonContainer}>
        <Button onPress={_onPressButton} title="This looks great!" />
        <Button onPress={_onPressPlus} title="+" color="#841584" />
      </View>
      <Button
        title="Go to Details"
        onPress={() => navigation.navigate('Details')}
      />
    </View>
  );
};

const DetailsScreen = () => {
  return (
    <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
      <Text>Details Screen</Text>
    </View>
  );
};

const App = () => {
  return (
      <Stack.Navigator initialRouteName="Home" >
        <Stack.Screen name="Home" component={HomeScreen} options={{ headerShown: false }} />
        <Stack.Screen name="Details" component={DetailsScreen} />
      </Stack.Navigator>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
  },
  buttonContainer: {
    margin: 20,
  },
  alternativeLayoutButtonContainer: {
    margin: 20,
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
});

export default App;
