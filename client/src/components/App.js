import { useEffect, useState } from "react";
import { BrowserRouter, Route, Switch, Redirect } from "react-router-dom";
import Home from "./Home";
import MessagesList from "./MessageList";
import NavBar from "./NavBar";
import Login from "./Login";
import Register from "./Register"

function App() {
 
  const [user, setUser] = useState(null);
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
  }, [])  

  if(isLoading) {
    return <div>Loading...</div>
  }

  return (
    <BrowserRouter>
      <NavBar user={user} setUser={setUser} />
      <div className="main-content">
          {user ? (
            <Switch>
              <Route path="/home" component={Home} />
              <Route path="/messages" component={MessagesList} />
              <Route path="*">
                <Redirect to="/home" />
              </Route>
            </Switch>
          ) : (
            <Switch>
              <Route path="/" exact>
                <Redirect to="/register" />
              </Route>
              <Route path="/login" 
                render = {(routeProps) => {
                  <Login {...routeProps} user={user} setUser={setUser} />
                }} 
              />
              <Route path="/register" 
                render = {(routeProps) => {
                  <Register {...routeProps} user={user} setUser={setUser} />
                }}  />
              <Route path="*">
                <Redirect to="/login" />
              </Route>
            </Switch>
          )}
      </div>
    </BrowserRouter>  
  );
}

export default App;
