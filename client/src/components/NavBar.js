import { useHistory } from "react-router-dom"
import { apiCall } from '../config'


const NavBar = ({ user, setUser }) => {
  const history = useHistory()

  const handleSignOut = () => {
    apiCall('/logout', {
      method: 'DELETE',
    }).then(() => {
      setUser(null)
      history.push('/home')
    })
  }

  // const handleLogin = () => {
  //   history.push('/login')
  // }



  return (
    <nav className='navbar'>
      <h1>CHATBOX</h1>
        {user ? (
          <button className="nav-button signout-button" onClick={handleSignOut}>
            Sign Out
          </button>) : null
        //   (
        //   <button className="nav-button login-button" onClick={handleLogin}>
        //     Login
        //   </button>
        // )}
        }
    </nav>
  )
}

export default NavBar