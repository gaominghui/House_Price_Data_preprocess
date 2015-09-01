
search <-function(file_name,train_dealdate_begin,train_dealdate_end,test_dealdate_begin,test_dealdate_end,filter_scale,regression_model){
    #print(file_name)
    #print(train_dealdate_begin)
    #print(train_dealdate_end)
    #print(test_dealdate_begin)
    #print(test_dealdate_end)
    #print(filter_scale)
    
    datas <- read.table(file_name,header=TRUE,fileEncoding="utf8")

    #datas <- datas[order(datas$build_end_year_ftr),]
    train_data <- subset(datas,  dealdate_ftr>=train_dealdate_begin & dealdate_ftr<=train_dealdate_end )

    train_data$unitprice<-train_data$realmoney/train_data$build_size

    meanunit <- mean(train_data$unitprice)
    train_data$subunit<-train_data$unitprice-meanunit
    train_data<-subset(train_data, abs(train_data$subunit)<meanunit*filter_scale)
    

    test_data <- subset(datas,dealdate_ftr>=test_dealdate_begin & dealdate_ftr<=test_dealdate_end)
    

    bj_house_model <- lm(regression_model,train_data)
        
    bj_cofficients_names=names(bj_house_model$coefficients)
    bj_cofficients = bj_house_model$coefficients
    
    save(bj_cofficients,file="ruliyouyichengCqu_parm.txt",eval.promises=FALSE,ascii=TRUE)
    
    bj_house_predict <- predict(bj_house_model,test_data,level=0.9,interval = "prediction")
    bj_house_predict <- as.data.frame(bj_house_predict)
    count=0
    test <-  abs(test_data$realmoney-exp(bj_house_predict$fit))
    pingjia <- test_data$realmoney
    percent <- test/test_data$realmoney*100
    
    result <- as.data.frame(test<=pingjia*0.05)
    #print(cbind(as.data.frame(test_data$house_code),as.data.frame(test_data$realmoney),as.data.frame(exp(bj_house_predict$fit)),as.data.frame(round(test)),as.data.frame(pingjia*0.05),result,percent))
    for (i in test<=pingjia*0.05){
        if(i){
            count<-count+1
        }
    }

    prec=count/nrow(test_data)
    ret=c(train_dealdate_begin,train_dealdate_end,test_dealdate_begin,test_dealdate_end,filter_scale)
    return(list(precision=prec,features=ret,cofficietns=bj_cofficients))
    

}


baoli_search <- function(file_name,current_date){
    best_answer=list(precision=0,features=c(),cofficients=list())
    feature_bixu<-c("bedroom_amount","parlor_amount","toilet_amount","log(build_size)","build_end_year_ftr_new","dealdate_ftr_new","fitment_ftr","face_ftr_new")
    feature_kexuan<-c("is_school_district_ftr","floor_ftr","floor_scale","total_floor_ftr","is_sales_tax_ftr","is_sole_ftr","uscale",
                   "balcony_amount_ftr","garden_amount_ftr","frame_structure_ftr")
    nl<-length(feature_kexuan)
    res<-lapply(1:nl,function(i) combn(feature_kexuan,i))

    models <- c()
    count=1
    for (temp in res){
        for(i in 1:ncol(temp)){
            models <-c(models,paste("log(realmoney) ~ ",paste(c(feature_bixu,temp[,i]),collapse="+")))
            count <- count+1     
        }

    }

    train_dealdate_begin <- c(1,2,3,4,5,6,7,8,9,10,11,12)
    train_dealdate_end <- c(1,2,3,4,5,6,7,8,9,10,11,12)
    test_dealdate_begin <- c(0,1)
    test_dealdate_end <- c(0,1)
    filter_scale <- c(0.5,0.4,0.3,0.2)


    for (train_begin in train_dealdate_begin){

        for(train_end in train_dealdate_end & train_end<=train_begin){
            
            for(test_begin in test_dealdate_begin & test_begin < train_end){
                
                for(test_end in test_dealdate_end &test_end<=test_begin){
                            
                    for(scale in filter_scale){

                        for(model in models){

                            answer=search(file_name="ruliyouyichengCqu.txt",train_dealdate_begin=current_date-train_begin,train_dealdate_end=current_date-train_end,test_dealdate_begin=current_date-test_begin,test_dealdate_end=current_date-test_end,filter_scale=scale,regression_model=model)				
                            if(!is.na(answer$precision) ){
				        if(answer$precision>best_answer$precision){
						best_answer=answer
					  }
                                
                            }
			      } 
                    }	
                }

            }
        
        }
    }




}
#search(file_name="ruliyouyichengCqu.txt",train_dealdate_begin=180,train_dealdate_end=186,test_dealdate_begin=187,test_dealdate_end=187,filter_scale=0.5,regression_model="")

best_model <- baoli_search("ruliyouyichengCqu.txt",187)
print(best_model$precision)
print(best_model$features)
print(best_model$cofficients)

