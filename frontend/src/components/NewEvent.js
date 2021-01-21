import React,{ useState } from 'react';
import axios from "axios";
import { Button, FormGroup, Label, Input,NavLink} from "reactstrap";


export default function NewEvent(props){
    const [email]=useState(sessionStorage.getItem("email"))
    const[title,setTitle]=useState(null);
    const[description,setDescription]=useState(null);
    const[date,setDate]=useState(null);
    const[error,setError]=useState(null);

    const createEvent=(e)=>{
        e.preventDefault();
        axios.post("http://localhost:8000/api/addevent",{
            title, description, date, creator:email
          }).then(res=>{
            setError(null);
            console.log(res.data);
            props.setNewEvent(false);
            props.setMsg("Event created successfully");
          }).catch(e=>{
              console.log(e)
            setError(e.response.data.msg);
          })
    }
    return(
        <form className="mt-3">
        <h6  style={{textAlign:"center",display:"inline"}}>New Event</h6>
        <NavLink
                    style={{display:"inline",padding:0,width:20}}
                    href="#"
                    onClick={()=>{props.setNewEvent(false)}}
                    className="my-0"
                    >
                   <h6 style={{color:"black",width:20,marginLeft:1050}}>X</h6>
                    </NavLink>
            <div className="form-row">
          <FormGroup className="col-md-6">
            <Label for="inputTitle">Title</Label>
            <Input type="text"  id="inputTitle" onChange={(e)=>{(e.target.value==="")?setTitle(null):setTitle(e.target.value)}}/>
          </FormGroup>
          <FormGroup className="col-md-6">
            <Label for="inputDescription">Description</Label>
            <Input type="text"  id="inputDescription" onChange={(e)=>{(e.target.value==="")?setDescription(null):setDescription(e.target.value)}}/>
          </FormGroup>
        </div>
            <div className="form-row">
          <FormGroup className="col-md-6 mx-auto">
            <Label for="inputDate">Date</Label>
            <Input type="date"  id="inputDate" onChange={(e)=>{setDate(e.target.value);console.log(e.target.value)}}/>
          </FormGroup>
        </div>
        <h6 style={{textAlign:"center",color: '#f60000'}}>{error}</h6>
        <Button  color="success" onClick={createEvent}>Create</Button>
        </form>
    )
}