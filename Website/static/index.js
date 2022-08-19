function deleteGift(giftID){
    fetch('/delete-gift', {
        method: 'POST',
        body: JSON.stringify({giftID: giftID})
    }).then((_res)=>{
        window.location.href = "/";
    });
}