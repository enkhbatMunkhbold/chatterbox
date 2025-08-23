import { useFormik } from 'formik'
import { useHistory, Link } from 'react-router-dom'
import * as Yup from 'yup'
import '../styling/register.css'
import { apiCall } from '../config'

const Register = ({ user, setUser }) => {
  const history = useHistory()

  const formik = useFormik({
    initialValues: {
      username: "",
      password: "",
      passwordConfirmation: ""
    },
    validationSchema: Yup.object({
      username: Yup.string()
        .required("Username is required")
        .min(3, "Username mast be at least 3 characters long"),
      pasword: Yup.string()
        .required("Password is required")
        .min(9, "Password must meb at least 9 characters long"),
      passwordConfirmation: Yup.string()
        .required("Password confirmation is required")
        .oneOf([Yup.ref('password')], "Passwords must match")
    }),
    onSubmit: (values) => {
      apiCall("/register", {
        method: "POST",
        body: JSON.stringify({
          username: values.username,
          password: values.password
        })
      })
      .then(async res=> {
        console.log("Registration response status:", res.status)
        console.log("Registration response headers:", res.headers)
        if(res.ok) {
          return res.json()
        } else {
          const errorData = await res.json()
          console.error("Server error response:", errorData)
          throw new Error(errorData.error || `Registration failed with status ${res.status}`)
        }
      })
      .then(user => {
        setUser(user)
        history.replace("/home")
      })
      .catch(error => {
        console.error("Registration error:", error)
        console.error("Error details:", {
          message: error.message,
          stack: error.stack
        })
        alert(`Registration failed: ${error.message}`)
      })
    }
  })

  return (
    <div className="auth-container">
      <form onSubmit={formik.handleSubmit} className='auth-form'>
        <h2>Register</h2>
        <div className='form-group'>
          <input 
            type="text"
            name="username"
            placeholder='Username'
            autoComplete='off'
            value={formik.values.username}
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
          />
          {formik.touched.username && formik.errors.username && (
            <p style={{ color: "red" }}>{formik.errors.username}</p>
          )}
        </div>
        <div className='form-group'>
          <input 
            type="password"
            name="password"
            placeholder='Password'
            value={formik.values.password}
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            autoComplete='new-password'
          />
          {formik.touched.password && formik.errors.password && (
            <p style={{ color: "red" }}>{formik.errors.password}</p>
          )}
        </div>
        <div className='form-group'>
          <input 
            type="password"
            name="passwordConfirmation"
            placeholder='Password Confirmation'
            value={formik.values.passwordConfirmation}
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            autoComplete='new-password'
          />
          {formik.touched.passwordConfirmation && formik.errors.passwordConfirmation && (
            <p style={{ color: "red" }}>{formik.errors.passwordConfirmation}</p>
          )}
        </div>
        <button type="submit">Register</button>
        <div className='auth-link'>
          Already have an account? <Link to="/login">Login</Link>
        </div>
      </form>
    </div>
  )
}

export default Register