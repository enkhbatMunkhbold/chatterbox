import { useEffect, useState } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Home from "./Home";
import MessagesList from "./MessageList";
import NavBar from "./NavBar";
import Login from "./Login";
import Register from "./Register"

function App() {
 
  const [user, setUser] = useState[null];
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    fetch('/check_session', {
      credentials: 'include'
    })
    .then((r) => {
      if(r.ok) {
        return r.json().then(user => {
          setUser(user)
          setIsLoading(false)
        })
      } else if(r.status === 204) {
        setUser(null)
      } else {
        throw new Error(`HTTP error! Status: ${r.status}`)
      }
    })
    .catch(error => {
      console.log("Error checking session:", error)
      setUser(null)
      setIsLoading(false)
    })
  }, [setUser])  

  if(isLoading) {
    return <div>Loading...</div>
  }

  return (
    <Router>
      <NavBar user={user} setUser={setUser} />
      <div className="main-content">
          {user ? (
            <Routes>
              <Route path="/home" element={<Home />} />
              <Route path="/messages" element={<MessagesList/>} />
              <Route path="*" element={<Navigate to="/home" replace />} />
            </Routes>
          ) : (
            <Routes>
              <Route path="/" element={<Navigate to="/register" replace />} />
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="*" element={<Navigate to="/login" replace />} />
            </Routes>
          )}
      </div>
    </Router>  
  );
}

export default App;
