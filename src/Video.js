import React, { Component } from 'react';
import axios from 'axios';
import {Progress} from 'reactstrap';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

class Video extends Component {
  constructor(props) {
    super(props);
    this.state = {
      packageId:"",
      dashUrl:"Null",
      key:"",
      kId:"",
      status:"No Package Id Entered"
    }
  }

  handleChange = async(e) =>{
    console.log(e.target.value);
    this.setState({ 
        packageId: e.target.value,
    })
  }

  returnBase64 = (stringVal) =>{
    var hexArray = stringVal.replace(/\r|\n/g, "").replace(/([\da-fA-F]{2}) ?/g, "0x$1 ").replace(/ +$/, "").split(" ");
    var byteString = String.fromCharCode.apply(null, hexArray);
    var base64string = window.btoa(byteString);
    return base64string;
  }

  fetchVideoInfo =  async()=>{
    await axios.get(`https://c35gbfabih.execute-api.us-east-1.amazonaws.com/prod/packaged_content/${this.state.packageId}`, {
        headers: {
          'x-api-key':'rakuten-prod-key-12345'
        }
      })
      .then((response) => {
        console.log(response);
        this.setState({ 
          status: response["data"]["videoStatus"],
          dashUrl: response.data.dashUrl && response.data.dashUrl
        })
        setTimeout(()=>{
            if(response.data.dashUrl){
                this.onPlayerhandler(this.returnBase64(response["data"]["keyVal"]), this.returnBase64(response["data"]["kidVal"]));
            }
                
        },10);
      })
      .catch((error) => {
      })
  }

  onPlayerhandler = async(keyVal,kidValue) => {
    keyVal=keyVal.replace("==","");
    kidValue=kidValue.replace("==","")
    console.log(kidValue);
    console.log(keyVal);
    debugger
    var clearKeyObject={  }
    clearKeyObject[`${kidValue}`]=keyVal
    const protData = {
        "org.w3.clearkey": {
            "clearkeys": clearKeyObject
        }
    };
    var video,
        player,
        url = this.state.dashUrl;

    video = document.querySelector("video");
    player =window.dashjs.MediaPlayer().create();
    player.initialize(video, url, true);
    player.setProtectionData(protData);
  }
  
  // Callback~
  async getFiles(files){
    
  }

  render() {
    return (
      <div class="container" style={{marginTop:'15px'}}>
      
        <div className="row">
          -------------------------------------------------------------------------
        </div>

        <div className="row">
          <div className="offset-md-3 col-md-6">
            <label style={{fontSize: "18px"}}>
              <b>Rakuten DASH Video Player</b>
            </label>
          </div>
        </div>

        <div className="row">
          <div><b>Enter Package ID To Play :</b></div>
          <br></br>
          <input style={{width:"500px"}} onChange={this.handleChange} value={this.state.packageId}></input>
        </div>

        <div className="row" style={{marginTop:'4px'}}>
          Media Package Status : <b>{this.state.status}</b>
          <b>{this.state.status=="ENCODE_STARTED" ? " -> IN PROGRESS" : " "}</b>
        </div>

        <div className="row" style={{marginTop:'4px'}}>
          Dash URl Returned : <input style={{width:"500px"}} value={this.state.dashUrl}></input>
        </div>

        <div className="row" style={{marginTop:'4px'}}>
          <div>
            <video controls="true"></video>
          </div>
        </div>

        <div className="row" style={{marginTop:'8px'}}>
          <div className="offset-md-3 col-md-6">
                <button type="button" className="btn btn-success btn-block" onClick={this.fetchVideoInfo}>
                   Play Video
                </button>
            </div>
        </div>
      </div>
    );
  }
}

export default Video;
