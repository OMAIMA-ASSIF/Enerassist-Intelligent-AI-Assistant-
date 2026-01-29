import { createContext, useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { dummyChats, dummyUserData } from "../../assets/assets";

const AppContext = createContext();

export const AppContextProvider = ({ children }) => {
    const navigate = useNavigate();

    const [user, setUser] = useState(null);
    const [chats, setChats] = useState([]);
    const [selectedChat, setSelectedChat] = useState(null);
    const [theme, setTheme] = useState(
        localStorage.getItem("theme") || "light"
    );


    const logout = () => {
        setUser(null)
        setChats([])
        setSelectedChat(null)
    }

    const createNewChat = () => {
        const newChat = {
            _id: Date.now(),
            name: "New Chat",
            messages: [],
            createdAt: new Date(),
            updatedAt: new Date(),
        }

        setChats(prev => [newChat, ...prev])
        setSelectedChat(newChat)
    }

    const deleteChat = (chatId) => {
        setChats(prev => prev.filter(chat => chat._id !== chatId))

        // si le chat supprimé est celui sélectionné
        setSelectedChat(prev =>
            prev?._id === chatId ? null : prev
        )
    }

    const fetchUser = async () => {
        setUser(dummyUserData);
    };

    const fetchUserChats = async () => {
        setChats(dummyChats);
        setSelectedChat(dummyChats[0]);
    };

    // Dark mode
    useEffect(() => {
        if (theme === "dark") {
            document.documentElement.classList.add("dark");
        } else {
            document.documentElement.classList.remove("dark");
        }
        localStorage.setItem("theme", theme);
    }, [theme]);

    // Load chats when user exists
    useEffect(() => {
        if (user) {
            fetchUserChats();
        } else {
            setChats([]);
            setSelectedChat(null);
        }
    }, [user]);

    // Initial user fetch
    useEffect(() => {
        fetchUser();
    }, []);

    const value = {
        navigate,
        user,
        setUser,
        fetchUser,
        chats,
        setChats,
        selectedChat,
        setSelectedChat,
        theme,
        setTheme,
        createNewChat,
        deleteChat,
        logout
    };

    return (
        <AppContext.Provider value={value}>
            {children}
        </AppContext.Provider>
    );
};
// 01:01:29
export const useAppContext = () => {
    return useContext(AppContext);
};