class Main inherits IO
{
   x : Int <- 5;
   y : Int <- 4;
   main() : Object {{
                y <- x+4;
		x<-7656; 
		out_int(x); 
		self;
	}};
};
