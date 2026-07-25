import {AppBar,Toolbar,Typography,Chip} from "@mui/material";

function Header(){

    return(

        <AppBar
            position="static"
            sx={{
                background:"#151C32",
                boxShadow:"none"
            }}
        >

            <Toolbar>

                <Typography
                    variant="h5"
                    sx={{flexGrow:1,fontWeight:"bold"}}
                >

                    QuantumShield Security Operations Center

                </Typography>

                <Chip
                    label="SYSTEM ONLINE"
                    color="success"
                />

            </Toolbar>

        </AppBar>

    )

}

export default Header;