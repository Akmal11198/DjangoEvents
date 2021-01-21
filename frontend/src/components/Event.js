import React,{useState,useEffect} from 'react';
import axios from "axios";
import { Card, Container, Row, Col, Button, ListGroup, ListGroupItem, Input} from "reactstrap";

export default function Event(props){
    const [email]=useState(sessionStorage.getItem("email"))
    const[event,setEvent]=useState(props.event);
    const[description,setDescription]=useState(null);
    const[date,setDate]=useState(null);
    const[edit,setEdit]=useState(false);
   useEffect(()=>{
    setEvent(props.event)
   },[props,email,edit])
    const join=()=>{
        axios.post("http://localhost:8000/api/joinevent",{
            email,
            title:event.title
        }).then(res=>{
            console.log(res.data);
            props.setMsg("Event joined successfully");
          }).catch(e=>{
            props.setError(e.response.data.msg);
          })
    }

    const save=()=>{
        axios.put("http://localhost:8000/api/editevent",{
            creator:email,
            date,description,
            title:event.title
        }).then(res=>{
            console.log(res.data);
            setEdit(false);
            props.setMsg("Event changes saved successfully");
          }).catch(e=>{
            props.setError(e.response.data.msg);
          })
    }

    const withdraw=()=>{
        axios.delete("http://localhost:8000/api/exitevent",{
            data:{
                email,
                title:event.title
            }
        }).then(res=>{
            console.log(res.data);
            props.setMsg("Withdrew from Event successfully");
          }).catch(e=>{
            props.setError(e.response.data.msg);
          })
    }
   

    return(
            <tr>
            <td>{event?event.title:"Loading..."}</td>
            <td>{event?(edit?
                (<Input type="text"  id="inputDescription" onChange={(e)=>{(e.target.value==="")?setDescription(null):
                setDescription(e.target.value)}}/>):
                event.description):"Loading..."}</td>
            <td>{event?(edit?(
                <Input type="date"  id="inputDate" onChange={(e)=>{setDate(e.target.value)}}/>
            ):event.date):"Loading..."}</td>
            <td>{event?event.creator:"Loading..."}</td>
            <td >{event?(edit?(<Button color="success" onClick={save}>Save</Button>):event.participants.length):"Loading..."}</td>
            <td >{event?(event.creator==email?(edit?(<Button onClick={()=>{setEdit(false)}}>Cancel</Button>):
                <Button color="primary" onClick={()=>{setEdit(true)}}>Edit</Button>):
                (event.participants.includes(email)?(<Button color="danger" onClick={withdraw}>Withdraw</Button>):
                (<Button color="success" onClick={join}>Join</Button>))):"Loading..."}</td>
            </tr>
        
    )
}