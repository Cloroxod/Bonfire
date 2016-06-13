package com.btores.bonfire;

import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import android.location.Location;

/**
 * Created by Zach on 6/11/2016.
 */
public class MessageFragment extends Fragment {
    /**
     * The fragment argument representing the section number for this
     * fragment.
     */
    private static final String ARG_SECTION_NUMBER = "section_number";

    /**
     * Returns a new instance of this fragment for the given section
     * number.
     */
    public static MessageFragment newInstance(int sectionNumber) {
        MessageFragment fragment = new MessageFragment();

        return fragment;
    }

    public MessageFragment() {
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View rootView = inflater.inflate(R.layout.fragment_message, container, false);
        

        return rootView;
    }

    public class LocationResultCallback {
        public void locationReceived(Location location){
            //do something with the coordinates
        }
    }

}