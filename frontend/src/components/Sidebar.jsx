import {
Drawer,
List,
ListItemButton,
ListItemIcon,
ListItemText
}
from "@mui/material";

import {
FaHome,
FaChartLine,
FaNetworkWired,
FaBell,
FaRobot
}
from "react-icons/fa";

const menu=[

["Dashboard",<FaHome/>],

["Live Monitor",<FaChartLine/>],

["Wallet Graph",<FaNetworkWired/>],

["Alerts",<FaBell/>],

["AI Engine",<FaRobot/>]

];

function Sidebar(){

return(

<Drawer
variant="permanent"
sx={{
    width:240,
    flexShrink:0,
    "& .MuiDrawer-paper":{
        width:240,
        background:"#151C32",
        color:"white",
        borderRight:"1px solid #27314E"
    }
}}
></Drawer>

)

}

export default Sidebar;