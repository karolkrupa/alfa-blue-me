#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <net/if.h>
#include <sys/ioctl.h>
#include <sys/socket.h>
#include <linux/can.h>
#include <linux/can/raw.h>

int main()
{
    int ret;
    int s, nbytes;
    struct sockaddr_can addr;
    struct ifreq ifr;
    struct can_frame frame, proxi_frame;
    memset(&proxi_frame, 0, sizeof(struct can_frame));
    proxi_frame.can_id = 0x123;
    proxi_frame.can_dlc = 6;
    proxi_frame.data[0] = 0x21;
    proxi_frame.data[1] = 0x14;
    proxi_frame.data[2] = 0x00;
    proxi_frame.data[3] = 0x28;
    proxi_frame.data[4] = 0x65;
    proxi_frame.data[5] = 0x70;
    
    memset(&frame, 0, sizeof(struct can_frame));

    printf("Proxi run\r\n");
    
    //1.Create socket
    s = socket(PF_CAN, SOCK_RAW, CAN_RAW);
    if (s < 0) {
        perror("socket PF_CAN failed");
        return 1;
    }
    
    //2.Specify can0 device
    strcpy(ifr.ifr_name, "can0");
    ret = ioctl(s, SIOCGIFINDEX, &ifr);
    if (ret < 0) {
        perror("ioctl failed");
        return 1;
    }

    //3.Bind the socket to can0
    addr.can_family = PF_CAN;
    addr.can_ifindex = ifr.ifr_ifindex;
    ret = bind(s, (struct sockaddr *)&addr, sizeof(addr));
    if (ret < 0) {
        perror("bind failed");
        return 1;
    }
    
    //4.Define receive rules
    struct can_filter rfilter[1];
    rfilter[0].can_id = 0x740;
    rfilter[0].can_mask = CAN_SFF_MASK;
    setsockopt(s, SOL_CAN_RAW, CAN_RAW_FILTER, &rfilter, sizeof(rfilter));

    //5.Receive data and exit
    while(1) {
        nbytes = read(s, &frame, sizeof(frame));
        if(nbytes > 0) {
            if(frame.can_id == 0x740) {
                printf("%s", "Proxi 0x740");
                //6.Send message
                nbytes = write(s, &proxi_frame, sizeof(proxi_frame));
                if(nbytes != sizeof(proxi_frame)) {
                    printf("Send Error frame[0]!\r\n");
                    close(s);
                    return 0;
                }
            }
//            printf("can_id = 0x%X\r\ncan_dlc = %d \r\n", frame.can_id, frame.can_dlc);
//            int i = 0;
//            for(i = 0; i < 8; i++)
//                printf("data[%d] = %d\r\n", i, frame.data[i]);
//            break;
        }
    }
    
    //6.Close the socket
    close(s);
    
    return 0;
}
