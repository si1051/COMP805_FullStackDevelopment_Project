import axios from 'axios';

export const createOrUpdateUser = async (userDetails, idToken) => {
    return await axios.post(
        `${process.env.REACT_APP_API}/createOrUpdateUser`,
        {
            userDetails
        },
        {
            headers: {
                idToken
            }
        }
    )
}

export const checkUser = async (email) => {
    return await axios.post(
        `${process.env.REACT_APP_API}/checkUserRole`,
        {
            email
        }
    )
}

export const currentUser = async (email, idToken) => {
    return await axios.post(
        `${process.env.REACT_APP_API}/getCurrentUser`,
        {
            email
        },
        {
            headers: {
                idToken
            }
        }
    )
}

export const getUsers = async (idToken) => {
    return await axios.get(
        `${process.env.REACT_APP_API}/getUsers`,
        {
            headers: {
                idToken
            }
        }
    )
}
