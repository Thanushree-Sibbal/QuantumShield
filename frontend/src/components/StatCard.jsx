import {Card,CardContent,Typography} from "@mui/material";

function StatCard({title,value}){

return(

<Card
sx={{
background:"#151C32",
color:"white",
border:"1px solid #27314E"
}}
>

<CardContent>

<Typography color="gray">

{title}

</Typography>

<Typography
variant="h4"
fontWeight="bold"
>

{value}

</Typography>

</CardContent>

</Card>

)

}

export default StatCard;