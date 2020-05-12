import React, { Component } from 'react';
import axios from 'axios';
import {Progress} from 'reactstrap';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import FileBase64 from 'react-file-base64';
import Video from './Video'
import OverlayLoader from 'react-overlay-loading/lib/OverlayLoader'

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      file:'',
      files: '',
      message:" ",
      videoID: " ",
      packageId: " ",
      loaded: 0,
      isLoading:false,
      key:"87237D20A19F58A740C05684E699B4AA",
      kid:"A16E402B9056E371F36D348AA62BB749",
      fileName:""
    }
  }

  updateDbHandler = async() => {
    let file = this.state.file;
    let requestObj = {
      'fileName': this.state.fileName,
      'fileType': file["type"],
      'fileSize': file["size"],
    }
    await axios.post("https://c35gbfabih.execute-api.us-east-1.amazonaws.com/prod/upload_input_content", requestObj, {
      headers: {
        'x-api-key':'rakuten-prod-key-12345'
      }
    })
    .then((response) => {
      console.log(response);
      this.setState({ 
        message:"File Successfuly Upload to Server",
        videoID: response["data"]["videoId"]
      })
    })
    .catch((error) => {
    })
    console.log("DONE")
  }

  getPresignedUrl = async() =>{
    //let fileName = this.state.files.file["name"]
    this.setState({ 
      isLoading: true
    })
    let fileName = new Date().getTime() + this.state.files.file["name"];  
    await axios.get(`https://c35gbfabih.execute-api.us-east-1.amazonaws.com/prod/fetchPresignedUrl?fileKey=${fileName}`, {
        headers: {
          'x-api-key':'rakuten-prod-key-12345'
        }
      })
      .then(async(response) => {
        this.setState({ 
          fileName:fileName
        })
        await this.uploadFileToS3(response.data, this.state.file);
        await this.updateDbHandler();
        this.setState({ 
          message:"File Successfuly Upload to Server",
          fileName:fileName,
          isLoading: false
        })
      })
      .catch((error) => {
      })
  }

  uploadFileToS3 = (presignedPostData, file) => {
    debugger
    return new Promise((resolve, reject) => {
      const formData = new FormData();
      Object.keys(presignedPostData.fields).forEach(key => {
        formData.append(key, presignedPostData.fields[key]);
      });
      
      // Actual file has to be appended last.
      debugger
      let newName = new Date().getTime() + file.name;  
      // formData.append('file[]', file, newName);
      var newFile = new File([file], newName , {type:file.type});
      formData.append("file", newFile);
      const xhr = new XMLHttpRequest();
      xhr.open("POST", presignedPostData.url, true);
      xhr.send(formData);
      xhr.onload = function() {
        console.log(this.status)
        this.status === 204 ? resolve() : reject(this.responseText);
      };
    });
  };

  // uploadMultipartFileUpload= async(url)=>{
  //   axios({
  //     method: "PUT",
  //     url: url,
  //     data: this.state.file,
  //     headers: { "Content-Type": "multipart/form-data" }
  //   })
  //     .then(res => {
  //         this.setState({
  //             uploadSuccess: "File upload successfull",
  //             error: undefined
  //         });
  //     })
  //     .catch(err => {
  //         this.setState({
  //             error: "Error Occured while uploading the file",
  //             uploadSuccess: undefined
  //         });
  //     });
  // }


  mediaPackageFunction = async() => {
    this.setState({ 
      isLoading: true
    })
    let requestObj = {
      'input_content_id': this.state.videoID,
      "key": this.state.key,
      "kid": this.state.kid 
    }
    await axios.post("https://c35gbfabih.execute-api.us-east-1.amazonaws.com/prod/packaged_content", requestObj, {
      headers: {
        'x-api-key':'rakuten-prod-key-12345'
      }
    })
    .then((response) => {
      console.log(response);
      this.setState({ 
        message:"File Encoded Request Sent for Background Processing",
        packageId:response.data["packaged_content_id"]
      })
      this.setState({ 
        isLoading: false
      })
    })
    .catch((error) => {
    })
    console.log("DONE")
  }
  
  // Callback~
  async getFiles(files){
    this.setState({ 
      files: files,
      file: files.file,
      message:"File Selected. Click on Upload to Upload it to Server." 
    })
  }

  handleKeyChange = async(e) =>{
    console.log(e.target.value);
    this.setState({ 
        key: e.target.value,
    })
  }

  handleKeyIdChange = async(e) =>{
    console.log(e.target.value);
    this.setState({ 
        kid: e.target.value,
    })
  }

  handleVideoIdChange = async(e) =>{
    console.log(e.target.value);
    this.setState({ 
        videoID: e.target.value,
    })
  }


  render() {
    return (
      <div class="container">
        <OverlayLoader 
              color={'red'} // default is white
              loader="ScaleLoader" // check below for more loaders
              text="Loading... Please wait!" 
              active={this.state.isLoading} 
              backgroundColor={'black'} // default is black
              opacity=".7" // default is .9  
              >

            <div className="row">
              <div className="offset-md-3 col-md-6">
                <label style={{fontSize: "20px"}}>
                  <b>Rakuten Media Encoder Platform</b>
                </label>
              </div>
            </div>

            <div className="row">
              <div className="offset-md-3 col-md-6">
                <label style={{fontSize: "16px"}}>
                  <b>Message</b> : {this.state.message}
                </label>
              </div>
            </div>

            <div className="row">
              <div className="offset-md-3 col-md-6">
                  <div className="form-group files">
                      <FileBase64  multiple={ false } onDone={ this.getFiles.bind(this) }/>
                    </div>  
                    <div className="form-group">
                      {/* <Progress max="100" color="success" value={this.state.loaded} >{Math.round(this.state.loaded,2) }%</Progress> */}
                    </div> 
                    <button type="button" className="btn btn-success btn-block" onClick={this.getPresignedUrl}>Upload</button>
                </div>
            </div>

            <div className="row" style={{marginTop:'5px'}}>
              <div className="offset-md-3 col-md-6">
                <label style={{fontSize: "16px"}}>
                  <b>Video Id From Server</b> : <input onChange={this.handleVideoIdChange} value={this.state.videoID} style={{width:'350px'}}></input>
                </label>
              </div>
            </div>

            <div className="row" style={{marginTop:'8px'}}>
              <div className="offset-md-3 col-md-6">
                <div className="row">
                  <div class="col-lg-6 col-md-6">
                    Key : <input onChange={this.handleKeyChange} value={this.state.key} style={{width:'80%'}}></input>
                  </div>
                  <div class="col-lg-6 col-md-6">
                    KID: <input onChange={this.handleKeyIdChange} value={this.state.kid} style={{width:'80%'}}></input>
                  </div>
                </div>
              </div>
            </div>

            <div className="row" style={{marginTop:'8px'}}>
              <div className="offset-md-3 col-md-6">
                    <button type="button" className="btn btn-success btn-block" onClick={this.mediaPackageFunction}>
                      Media Package Above Video ID with <b>KEY</b> and <b>KID</b>
                    </button>
                    <div style={{marginTop:'3px'}}><b>Package Id Server</b> : <input value={this.state.packageId} style={{width:'350px'}}></input></div>
                </div>
            </div>

            <div className="row">
              <div className="offset-md-3 col-md-6">
                <Video></Video>
              </div>
            </div>
        </OverlayLoader>
      </div>
    );
  }
}

export default App;
