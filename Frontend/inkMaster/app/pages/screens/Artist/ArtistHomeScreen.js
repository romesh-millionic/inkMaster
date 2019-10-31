import React, { Component } from 'react';
import {
  TouchableOpacity,
  Text,
  StyleSheet,
  View
} from 'react-native';

import firebase from 'react-native-firebase';

export default class ArtistHomeScreen extends React.Component {

      constructor() {
        super();
        this.unsubscriber = null;
        this.state = {
          user: null,
        };
      }

        state = { currentUser: firebase.auth() }

    render() {
      const { currentUser } = this.state
      return (
        <View style={styles.container}>
          <Text>
            Hi {currentUser && currentUser.email}!
          </Text>
          <Text>
            Artist
          </Text>
          <TouchableOpacity style={styles.button}>
              <Text style={styles.buttonText} onPress={this._showGallery}>Gallery</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.button}>
              <Text style={styles.buttonText} onPress={this._showImageUpload}>Upload tattoo</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.button}>
              <Text style={styles.buttonText} onPress={this._showAccSettings}>Account settings</Text>
          </TouchableOpacity>
        </View>

      );
    }
  
    _showGallery = () => {
      this.props.navigation.navigate('Gallery');
    };

    _showImageUpload = () => {
      this.props.navigation.navigate('ImageUpload');
    };

    _showAccSettings = () => {
      this.props.navigation.navigate('Settings');
    };
    
}

  const styles = StyleSheet.create({
    container : {
      flexGrow: 1,
      backgroundColor:'#EBEDEF',
      alignItems:'center',
      justifyContent :'center'
    },
    button: {
      width: 300,
      backgroundColor: "#641E16",
      borderColor: "black",
      borderRadius: 10,
      marginVertical: 10,
      paddingVertical: 13
    },
    buttonText: {
      fontSize: 16,
      fontWeight: "500",
      color: "#ffffff",
      textAlign: "center"
    }
  });
  