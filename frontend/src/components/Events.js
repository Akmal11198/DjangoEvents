import React,{useState,useEffect} from 'react';
import axios from "axios";
import {DropdownButton,Container,Dropdown,Button,Table} from "react-bootstrap";
import NewEvent from "./NewEvent";
import Event from "./Event";
import {Redirect} from "react-router-dom";

export default function Events() {
    const [email,setEmail]=useState(sessionStorage.getItem("email"))
    const [msg,setMsg]=useState(null)
    const [error,setError]=useState(null)
    const [events,setEvents]=useState([])
    const [newEvent,setNewEvent]=useState(false)
    const [filter,setFilter]=useState("joined")

    useEffect(()=>{
        setEmail(sessionStorage.getItem("email"));
        if(filter==='joined'){
            axios.get(`http://localhost:8000/api/joinedevents/${email}/`).then((res)=>{
                console.log(res.data)
                setEvents(res.data);
            }).catch(e=>{
                console.log(e.response.data.msg)
                setError(e.response.data.msg)
                setMsg(null)
            })
        }
        else if(filter==="created"){
            axios.get(`http://localhost:8000/api/createdevents/${email}/`).then((res)=>{
                console.log(res.data)
                setEvents(res.data);
            }).catch(e=>{
                console.log(e.response.data.msg)
                setError(e.response.data.msg)
                setMsg(null)
            })
        }
        else{
            axios.get("http://localhost:8000/api/events").then((res)=>{
                console.log(res.data)
                setEvents(res.data);
            }).catch(e=>{
                console.log(e.response.data.msg)
                setError(e.response.data.msg)
                setMsg(null)
            })
        }
        if(msg){
            setTimeout(()=>{setMsg(null)},3000);
        }
        if(error){
            setTimeout(()=>{setError(null)},3000);
        }
    },[filter,msg,error,email])
    if(!email)
    return(<Redirect  to={{pathname:"/"}}/>)

    return (
        <Container>
            <DropdownButton
            variant="outline-secondary"
            title="filter Events"
            id="input-group-dropdown-1"
            onSelect={(e)=>{setFilter(e)}}
            >
                <Dropdown.Item href="#" eventKey="joined">Joined Events</Dropdown.Item>
                <Dropdown.Item href="#" eventKey="created" >Created Events</Dropdown.Item>
                <Dropdown.Item href="#" eventKey="All" >All</Dropdown.Item>
            </DropdownButton>
            {newEvent?(<NewEvent setNewEvent={setNewEvent} setMsg={setMsg}/>):(<Button className="mt-3" color="success" onClick={(e)=>{setNewEvent(true)}}>Create New Event</Button>)}
            <h6 style={{color:"green"}}>{msg}</h6>
            <h6 style={{color:"red"}}>{error}</h6>
            <h6 >{filter} Events</h6>
            <Table striped bordered hover className="mt-3">
                <thead>
                    <tr>
                        <th>Title</th>
                        <th>Description</th>
                        <th>Date</th>
                        <th>Creator</th>
                        <th>Participants #</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                {events.map(event=>(
                    <Event event={event} setMsg={setMsg} setError={setError}/>
                  ))}
                </tbody>
            </Table>
            <Button className="mt-3 btn-danger" color="danger" onClick={(e)=>{sessionStorage.removeItem("email");setMsg("Logged out successfully")}}>Log Out</Button>
        </Container>
    )
}
